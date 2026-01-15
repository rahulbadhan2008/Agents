# LLM Ops RAG Pipeline

![CI/CD](https://github.com/rahulbadhan2008/Agents/actions/workflows/main.yml/badge.svg)
![Monitoring](https://img.shields.io/badge/Monitoring-LangSmith-orange)
![License](https://img.shields.io/badge/License-MIT-blue)

A professional-grade End-to-End RAG pipeline featuring multi-agent orchestration via LangGraph and deep observability through LangSmith.

## 🚀 Features
- **Advanced Orchestration**: Super-Agent (LangGraph) manages a dynamic graph of sub-agents (Retrieval, Reranking, Synthesis).
- **Deep Observability**: Out-of-the-box LangSmith integration for tracing every decision and tool call.
- **Enterprise Search**: Hybrid search combining OpenSearch (Keyword/Vector) and Neo4j (Graph).
- **Scalable Infrastructure**: MVC architecture with FastAPI, ready for EC2/ECS deployment.
- **Robust MLOps**: CI/CD pipeline with linting, security scans, and automated testing.

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
- [API Documentation](api_documentation.md)
- [System Design](system_design.md)
- [Architecture Details](architecture.md)
- [Implementation Plan](.gemini/antigravity/brain/8e5993f9-7907-4f05-befb-fe0e15b9e1c9/implementation_plan.md)
- [Walkthrough](.gemini/antigravity/brain/8e5993f9-7907-4f05-befb-fe0e15b9e1c9/walkthrough.md)
