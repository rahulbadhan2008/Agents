from typing import Annotated, List, Union, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from .bedrock_service import bedrock_service
from .search_service import search_service
from .memory_service import MemoryService
from sqlalchemy.orm import Session

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]
    context: Dict[str, Any]
    next_step: str
    session_id: str
    agent_id: str

from .mcp_server import MCPServer
from langchain_core.utils.function_calling import convert_to_openai_tool

class SuperAgent:
    def __init__(self, db: Session, agent_id: str):
        self.db = db
        self.agent_id = agent_id
        self.llm = bedrock_service.get_llm()
        self.mcp = MCPServer(db)
        
        # Load tools dynamic from DB for this agent
        self.tools_metadata = self.mcp.load_tools(agent_id)
        
        # Bind tools to LLM if available
        if self.tools_metadata:
            self.llm_with_tools = self.llm.bind_tools([convert_to_openai_tool(t) for t in self.tools_metadata])
        else:
            self.llm_with_tools = self.llm
            
        self.workflow = self._create_workflow()

    def _create_workflow(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("plan_and_tool", self.plan_and_tool_node)
        workflow.add_node("execute_tools", self.execute_tools_node)
        workflow.add_node("synthesize", self.synthesize_node)

        workflow.set_entry_point("plan_and_tool")
        
        workflow.add_conditional_edges(
            "plan_and_tool",
            self.should_continue,
            {
                "continue": "execute_tools",
                "end": "synthesize"
            }
        )
        
        workflow.add_edge("execute_tools", "plan_and_tool")
        workflow.add_edge("synthesize", END)

        return workflow.compile()

    def plan_and_tool_node(self, state: AgentState):
        messages = state["messages"]
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def should_continue(self, state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"
        return "end"

    async def execute_tools_node(self, state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        
        tool_outputs = []
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            arguments = tool_call["args"]
            
            # Execute tool via MCP
            output = await self.mcp.call_tool(tool_name, **arguments)
            
            from langchain_core.messages import ToolMessage
            tool_outputs.append(ToolMessage(
                content=str(output),
                tool_call_id=tool_call["id"]
            ))
            
        return {"messages": tool_outputs}

    def synthesize_node(self, state: AgentState):
        messages = state["messages"]
        # LLM summarizes the conversation so far
        response = self.llm.invoke(messages)
        return {"messages": [response]}

from ..utils.caching import cache_service
from .sub_agents import RetrievalAgent, SynthesisAgent

    async def execute(self, session_id: str, agent_id: str, query: str):
        from ...models.models import ExecutionLog
        import datetime
        import uuid
        from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

        # Unique Trace ID for LangSmith
        trace_id = f"trace-{uuid.uuid4()}"
        
        # 1. Check Cache
        cache_key = cache_service.generate_cache_key(query, agent_id)
        cached_response = cache_service.get(cache_key)
        if cached_response:
            return cached_response

        execution_id = str(uuid.uuid4())
        
        # 2. Plan and Execute via LangGraph with Tracing
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "context": {},
            "next_step": "plan",
            "session_id": session_id,
            "agent_id": agent_id
        }
        
        cloudwatch_logger.log(f"Agent {agent_id} starting execution {execution_id} | Trace: {trace_id}", level="INFO")
        
        try:
            # LangGraph execution with recursive capability
            config = {"configurable": {"thread_id": session_id}, "run_name": f"SuperAgent-{agent_id}", "metadata": {"trace_id": trace_id}}
            result = await self.workflow.ainvoke(initial_state, config=config)

            # 3. Store in Cache (1 hour)
            cache_service.set(cache_key, result, expire=3600)
            
            # 4. Detailed Audit Trail
            log_entry = ExecutionLog(
                id=execution_id,
                agent_id=agent_id,
                query=query,
                response=result["messages"][-1].content,
                plan={"steps": ["plan", "retrieve", "synthesize"]},
                metrics={"latency": 0.0, "tokens": 0},
                trace_id=trace_id,
                created_at=datetime.datetime.utcnow()
            )
            self.db.add(log_entry)
            self.db.commit()
            
            cloudwatch_logger.log(f"Agent {agent_id} completed execution {execution_id}", level="INFO")
            return result
            
        except Exception as e:
            cloudwatch_logger.log(f"Execution failed: {str(e)}", level="ERROR")
            raise e
