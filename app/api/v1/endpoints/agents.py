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

@router.post("/")
def create_agent(request: CreateAgentRequest, db: Session = Depends(get_db)):
    manager = get_prompt_manager(db)
    agent_id = manager.create_agent(
        name=request.name,
        agent_type=request.type,
        system_prompt=request.system_prompt,
        config=request.config
    )
    return {"agent_id": agent_id}

@router.put("/{agent_id}/prompt")
def update_agent_prompt(agent_id: str, request: UpdatePromptRequest, db: Session = Depends(get_db)):
    manager = get_prompt_manager(db)
    success = manager.update_agent_prompt(agent_id, request.prompt)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Prompt updated successfully"}
