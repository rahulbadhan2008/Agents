from fastapi import FastAPI
from .api.v1.api import api_router
from .db.session import engine
from .models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LLM Ops RAG API",
    description="End-to-End RAG Pipeline with Multi-Agent Orchestration",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the LLM Ops RAG API"}
