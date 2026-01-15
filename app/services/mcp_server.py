from typing import Dict, Any, List
import json
import importlib.util
from sqlalchemy.orm import Session
from ..models.models import Tool

class MCPServer:
    """
    Model Context Protocol (MCP) Server implementation for handling dynamic tools.
    """
    def __init__(self, db: Session):
        self.db = db
        self.active_tools: Dict[str, Any] = {}

    def load_tools(self, agent_id: str):
        """Load tools assigned to a specific agent from the DB."""
        from ..models.models import Agent
        agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return []
            
        tools_metadata = []
        for tool in agent.tools:
            self._register_tool_logic(tool)
            tools_metadata.append({
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.schema
            })
        return tools_metadata

    def _register_tool_logic(self, tool_record: Tool):
        """Dynamically execute tool code and register it."""
        try:
            # Simple execution of stored code - in production, use a sandboxed environment
            local_namespace = {}
            exec(tool_record.code, {}, local_namespace)
            
            # Expecting a function with the same name as tool_record.name
            if tool_record.name in local_namespace:
                self.active_tools[tool_record.name] = local_namespace[tool_record.name]
        except Exception as e:
            print(f"Failed to register tool {tool_record.name}: {e}")

    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a registered tool."""
        if tool_name not in self.active_tools:
            raise ValueError(f"Tool {tool_name} not found or not registered.")
            
        func = self.active_tools[tool_name]
        # Handle both sync and async functions
        import inspect
        if inspect.iscoroutinefunction(func):
            return await func(**kwargs)
        return func(**kwargs)

def get_mcp_server(db: Session):
    return MCPServer(db)
