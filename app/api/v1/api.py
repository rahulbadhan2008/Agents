from fastapi import APIRouter
from .endpoints import rag, agents

api_router = APIRouter()
api_router.include_router(rag.router, prefix="/rag", tags=["RAG"])
api_router.include_router(agents.router, prefix="/agents", tags=["Agents"])
