# LLM Ops RAG Pipeline

![CI/CD](https://github.com/rahulbadhan2008/Agents/actions/workflows/main.yml/badge.svg)
![Monitoring](https://img.shields.io/badge/Monitoring-LangSmith-orange)
![License](https://img.shields.io/badge/License-MIT-blue)

A professional-grade End-to-End RAG pipeline featuring multi-agent orchestration via LangGraph and deep observability through LangSmith.

## 🚀 Features
- **Planning & Orchestration**: A specialized **Planning Agent** uses LangGraph to decompose user queries and assign tasks to specialized sub-agents.
- **Human-in-the-Loop (HITL)**: Intelligent detection of critical actions requiring manual human approval via specialized API endpoints.
- **DynamoDB Integration**: User-defined agents are stored in AWS DynamoDB for high scalability.
- **Continuous Learning Loop**: A tiered memory system (Temp, Short, Long) that automatically aggregates history into the Bedrock fine-tuning pipeline.
- **Enterprise Search**: Hybrid engine combining OpenSearch (BM25/Vector) and Neo4j (Graph).

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
