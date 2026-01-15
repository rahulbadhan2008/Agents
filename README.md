# LLM Ops RAG Pipeline

A comprehensive End-to-End RAG (Retrieval-Augmented Generation) pipeline built with AWS Bedrock, FastAPI, and LangChain.

## Features
- **Multi-Agent Orchestration**: Super-Agent managing specialized sub-agents via LangGraph.
- **Hybrid Search**: Combines OpenSearch (BM25 + KNN) and Neo4j (Graph).
- **Tiered Memory**: Managed session memory (Temp, Short-Term, Long-Term).
- **MLOps Ready**: CloudWatch logging, cost management, and CI/CD templates.

## Setup
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd Agents
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   - Copy `.env.example` to `.env`.
   - Update your AWS and Database credentials.

4. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Documentation
- [System Design](system_design.md)
- [Architecture Details](architecture.md)
- [Implementation Plan](.gemini/antigravity/brain/8e5993f9-7907-4f05-befb-fe0e15b9e1c9/implementation_plan.md)
- [Walkthrough](.gemini/antigravity/brain/8e5993f9-7907-4f05-befb-fe0e15b9e1c9/walkthrough.md)
