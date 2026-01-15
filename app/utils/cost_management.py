from sqlalchemy.orm import Session
from ..models.models import Agent, AgentType
from datetime import datetime
from .logging import cloudwatch_logger

class CostManager:
    def __init__(self, db: Session):
        self.db = db

    def cleanup_temporary_agents(self):
        """Delete temporary agents that have expired (8h default)."""
        expired_agents = self.db.query(Agent).filter(
            Agent.type == AgentType.TEMPORARY,
            Agent.expires_at < datetime.utcnow()
        ).all()
        
        count = len(expired_agents)
        for agent in expired_agents:
            self.db.delete(agent)
            cloudwatch_logger.log(f"Deleted expired temporary agent: {agent.id}", level="INFO")
            
        self.db.commit()
        return count

    def get_usage_metrics(self, agent_id: str):
        # In a real app, this would query Bedrock/CloudWatch for token usage
        return {
            "agent_id": agent_id,
            "estimated_cost": 0.05, # Mock value
            "tokens_used": 1500
        }

def get_cost_manager(db: Session):
    return CostManager(db)
