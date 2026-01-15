# LLM Ops RAG API Documentation

This document provides detailed specifications for the available API endpoints in the LLM Ops RAG Pipeline.

## Base URL
`http://localhost:8000/api/v1`

## RAG Endpoints

### Execute RAG Query
Executes a multi-agent RAG workflow including retrieval, reranking, and synthesis.

- **URL**: `/rag/query`
- **Method**: `POST`
- **Authentication**: None (Add API Key in production)
- **Request Body**:
  ```json
  {
    "query": "What are the benefits of hybrid search?",
    "session_id": "session-123",
    "agent_id": "agent-default"
  }
  ```
- **Success Response (200 OK)**:
  ```json
  {
    "query": "What are the benefits of hybrid search?",
    "response": "Hybrid search combines keyword and vector search...",
    "context": {
      "bm25": [...],
      "vector": [...],
      "graph": [...]
    }
  }
  ```

---

## Agent Management Endpoints

### Create Agent
Creates a new parametric or temporary agent with a specific system prompt.

- **URL**: `/agents/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "name": "Research Assistant",
    "type": "parametric",
    "system_prompt": "You are a research expert...",
    "config": {
      "temperature": 0.05
    }
  }
  ```
- **Success Response (200 OK)**:
  ```json
  {
    "agent_id": "uuid-v4-string"
  }
  ```

### Update Agent Prompt
Dynamically update the system prompt for an existing agent.

- **URL**: `/agents/{agent_id}/prompt`
- **Method**: `PUT`
- **Request Body**:
  ```json
  {
    "prompt": "Your updated system instructions here..."
  }
  ```
- **Success Response (200 OK)**:
  ```json
  {
    "message": "Prompt updated successfully"
  }
  ```

---

## Technical Specifications
- **Framework**: FastAPI
- **Architecture**: MVC (Model-View-Controller)
- **Validation**: Pydantic v2
- **Persistence**: PostgreSQL (SQLAlchemy) & Redis
