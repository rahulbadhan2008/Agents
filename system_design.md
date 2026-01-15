# System Design: LLM Ops RAG Pipeline

## Components

### 1. Planning Layer (LangGraph)
- **Planning Agent**: Analyzes user intent and generates a multi-step task list.
- **Sub-Agents**: Independent workers for Retrieval, Reranking, and Synthesis.
- **HITL Interceptor**: Pauses execution for critical regions, awaiting human approval.

### 2. Storage Layer (Hybrid)
- **DynamoDB**: Primary store for Agent metadata and tool definitions.
- **PostgreSQL**: Stores execution logs, audit trails, and memory layers.
- **Redis**: Low-latency cache for query results.

### 3. Search Engine (Hybrid)
- **OpenSearch**: Keyword (BM25) and Semantic (KNN) search.
- **Neo4j**: Graph-based relationship retrieval.

### 4. Memory Tiers
- **Temp (8h)**: Session-scoped cache.
- **Short-Term (7d)**: Contextual persistence.
- **Long-Term**: Persistent history for fine-tuning.

### 5. Training Pipeline
- Automated data extraction from long-term memory.
- Fine-tuning dataset preparation for Bedrock models.

### 6. MLOps & CI/CD
- **Linting & Security**: Automated code quality (flake8) and security (bandit) checks.
- **Observability**: Real-time tracing of agent planners and sub-agent executions in LangSmith.
- **Continuous Deployment**: Infrastructure templates for AWS ECS with CloudWatch monitoring integrations.

## Data Lifecycle
1. **Ingestion**: Documents are cleaned and chunked using `ChunkingUtility`.
2. **Retrieval**: Multi-model retrieval via OpenSearch and Neo4j.
3. **Synthesis**: LLM-based answer generation with audit trails.
4. **Maintenance**: Auto-cleanup of expired sessions and temporary agents.
