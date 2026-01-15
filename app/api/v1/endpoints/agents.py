from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ....db.session import get_db
from ....services.prompt_manager import get_prompt_manager
from ....models.models import AgentType
from pydantic import BaseModel

router = APIRouter()

class CreateAgentRequest(BaseModel):
    name: str
    type: AgentType
    system_prompt: str
    config: dict = None

class UpdatePromptRequest(BaseModel):
    prompt: str

from ....services.dynamodb_service import dynamodb_service

@router.post("/")
def create_agent(request: CreateAgentRequest, db: Session = Depends(get_db)):
    import uuid
    agent_id = str(uuid.uuid4())
    agent_data = {
        "agent_id": agent_id,
        "name": request.name,
        "type": request.type.value,
        "system_prompt": request.system_prompt,
        "config": request.config or {}
    }
    dynamodb_service.save_agent(agent_data)
    return {"agent_id": agent_id}

class CreateToolRequest(BaseModel):
    name: str
    description: str
    schema: dict
    code: str

@router.post("/tools")
def create_tool(request: CreateToolRequest, db: Session = Depends(get_db)):
    from ....models.models import Tool
    import uuid
    tool_id = str(uuid.uuid4())
    new_tool = Tool(
        id=tool_id,
        name=request.name,
        description=request.description,
        schema=request.schema,
        code=request.code
    )
    db.add(new_tool)
    db.commit()
    return {"tool_id": tool_id}

@router.post("/{agent_id}/tools/{tool_id}")
def assign_tool_to_agent(agent_id: str, tool_id: str, db: Session = Depends(get_db)):
    from ....models.models import Agent, Tool
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not agent or not tool:
        raise HTTPException(status_code=404, detail="Agent or Tool not found")
    
    agent.tools.append(tool)
    db.commit()
    return {"message": "Tool assigned successfully"}
