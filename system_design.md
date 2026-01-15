# System Design: LLM Ops RAG Pipeline

## Components

### 1. API Layer (FastAPI)
- Multi-controller setup (MVC).
- Endpoints for RAG queries and agent management.

### 2. Orchestration Layer (LangGraph)
- **Super-Agent**: High-level planner.
- **Sub-Agents**: Specialized roles for retrieval, reranking, and synthesis.

### 3. Search Engine (Hybrid)
- **OpenSearch**: Keyword (BM25) and Semantic (KNN) search.
- **Neo4j**: Graph-based relationship retrieval.

### 4. Memory Tiers
- **Temp (8h)**: Session-scoped cache.
- **Short-Term (7d)**: Contextual persistence.
- **Long-Term**: Persistent history for fine-tuning.

### 5. Training Pipeline
- Automated data extraction from long-term memory.
- Fine-tuning dataset preparation for Bedrock.
