```mermaid
graph TD
    User["User Query"] --> API["FastAPI Endpoint"]
    API --> SuperAgent["Super-Agent (LangGraph)"]
    
    subgraph "Orchestration & Tracing"
        SuperAgent --> LS["LangSmith (Deep Tracing)"]
        SuperAgent --> Plan["Planning Node"]
        Plan --> RetrievalAgent["Retrieval Sub-Agent"]
        RetrievalAgent --> LocalSearch["Hybrid Search Service"]
        LocalSearch --> OS["OpenSearch (BM25 + Vector)"]
        LocalSearch --> Neo4j["Neo4j (Graph)"]
        
        RetrievalAgent --> Rerank["Reranking Sub-Agent"]
        Rerank --> Synthesize["Synthesis Node"]
    end
    
    Synthesize --> Bedrock["AWS Bedrock LLM"]
    Bedrock --> Response["Final Answer"]
    
    subgraph "MLOps & CI/CD"
        MainJob[".github/workflows/main.yml"]
        MainJob --> Lint["Lint & Security"]
        MainJob --> Test["PyTest Suite"]
        MainJob --> Deploy["ECS Deployment"]
    end
    
    subgraph "Memory & Persistence"
        SuperAgent --> Cache["Redis Cache"]
        SuperAgent --> DB["PostgreSQL (Agents/Logs/Memory)"]
        DB --> FineTune["Fine-tuning Pipeline"]
    end
    
    Response --> User
```

## Monitoring & Tracing
Integrated **LangSmith** provides visibility into:
- Agent planning logic and task assignment.
- Sub-agent latency and execution IDs.
- Input/Output traces for all Bedrock calls.
- Cost tracking per query session.
