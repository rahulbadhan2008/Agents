# Architecture Overview

```mermaid
graph TD
    User["User Query"] --> API["FastAPI Endpoint"]
    API --> SuperAgent["Super-Agent (LangGraph)"]
    
    subgraph "Orchestration"
        SuperAgent --> Plan["Planning"]
        Plan --> RetrievalAgent["Retrieval Sub-Agent"]
        RetrievalAgent --> LocalSearch["Hybrid Search Service"]
        LocalSearch --> OS["OpenSearch (BM25 + Vector)"]
        LocalSearch --> Neo4j["Neo4j (Graph)"]
        
        RetrievalAgent --> Rerank["Reranking Sub-Agent"]
        Rerank --> Synthesize["Synthesis Sub-Agent"]
    end
    
    Synthesize --> Bedrock["AWS Bedrock LLM"]
    Bedrock --> Response["Final Answer"]
    
    subgraph "Memory & Persistence"
        SuperAgent --> Cache["Redis Cache"]
        SuperAgent --> DB["PostgreSQL (Agents/Logs/Memory)"]
        DB --> FineTune["Fine-tuning Pipeline"]
    end
    
    Response --> User
```

## Workflows
1. **Query Processing**: User submits a query -> Super-Agent plans -> Sub-agents retrieve and rerank -> LLM synthesizes answer.
2. **Memory Management**: Sessions are tracked; expired memories are auto-deleted.
3. **Audit Trail**: Every execution is logged to PostgreSQL and CloudWatch with unique Trace IDs.
