from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from .session import Base
import datetime
import enum

class AgentType(enum.Enum):
    SUPER = "super"
    PARAMETRIC = "parametric"
    TEMPORARY = "temporary"
    SUB = "sub"

class MemoryTier(enum.Enum):
    TEMP = "temp"
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Enum, Text, Table
from sqlalchemy.orm import relationship

# Association table for Agents and Tools
agent_tools = Table(
    "agent_tools",
    Base.metadata,
    Column("agent_id", String, ForeignKey("agents.id"), primary_key=True),
    Column("tool_id", String, ForeignKey("tools.id"), primary_key=True)
)

class Tool(Base):
    __tablename__ = "tools"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    schema = Column(JSON) # JSON Schema for tool arguments
    code = Column(Text) # Python code or logic for the tool
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    agents = relationship("Agent", secondary=agent_tools, back_populates="tools")

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(Enum(AgentType))
    system_prompt = Column(Text)
    config = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    tools = relationship("Tool", secondary=agent_tools, back_populates="agents")

class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    query = Column(Text)
    response = Column(Text)
    plan = Column(JSON) # Agent's plan
    metrics = Column(JSON) # Latency, tokens, cost
    trace_id = Column(String) # LangSmith trace ID
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    tier = Column(Enum(MemoryTier))
    content = Column(JSON) # {query: ..., response: ...}
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime)
