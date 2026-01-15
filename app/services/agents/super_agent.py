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
        from langchain_core.messages import HumanMessage

        trace_id = f"trace-{uuid.uuid4()}"
        cache_key = cache_service.generate_cache_key(query, agent_id)
        cached_response = cache_service.get(cache_key)
        if cached_response:
            return cached_response

        execution_id = str(uuid.uuid4())
        
        # Determine if action is critical for HITL
        is_critical = self._check_if_critical(query)

        initial_state = {
            "messages": [HumanMessage(content=query)],
            "context": {},
            "next_step": "plan",
            "session_id": session_id,
            "agent_id": agent_id,
            "requires_approval": is_critical
        }
        
        cloudwatch_logger.log(f"Agent {agent_id} starting Planning flow | Trace: {trace_id}", level="INFO")
        
        try:
            config = {"configurable": {"thread_id": session_id}, "run_name": f"PlanningAgent-{agent_id}", "metadata": {"trace_id": trace_id}}
            
            # Workflow with potential HITL interruption
            result = await self.workflow.ainvoke(initial_state, config=config)

            # Continuous Learning: Store in Long-Term Memory for fine-tuning pipeline
            from ..memory_service import MemoryService, MemoryTier
            from ..db.session import SessionLocal
            with SessionLocal() as db:
                memory_service = MemoryService(db)
                memory_service.add_memory(
                    session_id=session_id,
                    tier=MemoryTier.LONG_TERM,
                    content={"query": query, "response": result["messages"][-1].content, "agent_id": agent_id}
                )

            cache_service.set(cache_key, result, expire=3600)
            return result
            
        except Exception as e:
            cloudwatch_logger.log(f"Planning Agent failed: {str(e)}", level="ERROR")
            raise e

    def _check_if_critical(self, query: str) -> bool:
        # Simple logic: Tool calls or financial/system changes are critical
        critical_keywords = ["delete", "update", "transfer", "execute code"]
        return any(kw in query.lower() for kw in critical_keywords)

    def planning_node(self, state: AgentState):
        """Dedicated Planning node that assigns tasks to sub-agents."""
        messages = state["messages"]
        last_message = messages[-1].content
        
        # LLM creates a plan: "1. Search for X, 2. Rerank Y"
        plan_prompt = f"Based on the user query, create a detailed task plan for sub-agents: {last_message}"
        plan = self.llm.invoke([HumanMessage(content=plan_prompt)])
        
        return {"messages": [plan], "next_step": "execute_tools"}
