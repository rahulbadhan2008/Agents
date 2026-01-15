from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..models.models import Memory, MemoryTier
import json

class MemoryService:
    def __init__(self, db: Session):
        self.db = db

    def add_memory(self, session_id: str, tier: MemoryTier, content: dict):
        expires_at = None
        if tier == MemoryTier.TEMP:
            expires_at = datetime.utcnow() + timedelta(hours=8)
        elif tier == MemoryTier.SHORT_TERM:
            expires_at = datetime.utcnow() + timedelta(days=7)
        # Long term doesn't expire by default in this logic

        memory = Memory(
            session_id=session_id,
            tier=tier,
            content=content,
            expires_at=expires_at
        )
        self.db.add(memory)
        self.db.commit()

    def get_memories(self, session_id: str, tier: MemoryTier = None):
        query = self.db.query(Memory).filter(Memory.session_id == session_id)
        if tier:
            query = query.filter(Memory.tier == tier)
        
        # Filter out expired memories
        query = query.filter((Memory.expires_at == None) | (Memory.expires_at > datetime.utcnow()))
        
        return query.all()

    def promote_memory(self, session_id: str, source_tier: MemoryTier, target_tier: MemoryTier):
        """Move important context from temporary/short-term to long-term for learning."""
        memories = self.get_memories(session_id, source_tier)
        for mem in memories:
            new_memory = Memory(
                session_id=session_id,
                tier=target_tier,
                content=mem.content,
                expires_at=None if target_tier == MemoryTier.LONG_TERM else datetime.utcnow() + timedelta(days=7)
            )
            self.db.add(new_memory)
        self.db.commit()

    def get_all_long_term_for_fine_tuning(self):
        """Fetch all historical data for the fine-tuning pipeline."""
        return self.db.query(Memory).filter(Memory.tier == MemoryTier.LONG_TERM).all()
