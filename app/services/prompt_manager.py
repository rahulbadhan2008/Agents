from sqlalchemy.orm import Session
from ..models.models import Agent, AgentType
import uuid

class PromptManager:
    def __init__(self, db: Session):
        self.db = db

    def get_agent_prompt(self, agent_id: str):
        agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
        return agent.system_prompt if agent else "Default system prompt."

    def update_agent_prompt(self, agent_id: str, new_prompt: str):
        agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
        if agent:
            agent.system_prompt = new_prompt
            self.db.commit()
            return True
        return False

    def create_agent(self, name: str, agent_type: AgentType, system_prompt: str, config: dict = None):
        agent_id = str(uuid.uuid4())
        new_agent = Agent(
            id=agent_id,
            name=name,
            type=agent_type,
            system_prompt=system_prompt,
            config=config or {}
        )
        self.db.add(new_agent)
        self.db.commit()
        return agent_id

def get_prompt_manager(db: Session):
    return PromptManager(db)
