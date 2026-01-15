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

class SuperAgent:
    def __init__(self, db: Session):
        self.db = db
        self.llm = bedrock_service.get_llm()
        self.workflow = self._create_workflow()

    def _create_workflow(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("plan", self.plan_node)
        workflow.add_node("retrieve", self.retrieve_node)
        workflow.add_node("synthesize", self.synthesize_node)

        workflow.set_entry_point("plan")
        workflow.add_edge("plan", "retrieve")
        workflow.add_edge("retrieve", "synthesize")
        workflow.add_edge("synthesize", END)

        return workflow.compile()

    def plan_node(self, state: AgentState):
        # Implementation of planning logic
        return {"next_step": "retrieve"}

    def retrieve_node(self, state: AgentState):
        query = state["messages"][-1].content
        # Hybrid search
        results = search_service.hybrid_search(query)
        return {"context": results}

import json

    def synthesize_node(self, state: AgentState):
        context = state.get("context", {})
        query = state["messages"][-1].content
        
        # Simple synthesis for now
        prompt = f"Context: {json.dumps(context, indent=2)}\n\nQuery: {query}"
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
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
