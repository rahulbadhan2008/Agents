from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ....db.session import get_db
from ....services.agents.super_agent import SuperAgent
from ....services.memory_service import get_memory_service
from pydantic import BaseModel

router = APIRouter()

class RAGRequest(BaseModel):
    query: str
    session_id: str
    agent_id: str

@router.post("/query")
async def execute_rag_query(request: RAGRequest, db: Session = Depends(get_db)):
    super_agent = SuperAgent(db, request.agent_id)
    try:
        result = await super_agent.execute(
            session_id=request.session_id,
            agent_id=request.agent_id,
            query=request.query
        )
        return {
            "query": request.query,
            "response": result["messages"][-1].content,
            "context": result["context"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
