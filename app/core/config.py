from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "your_access_key")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "your_secret_key")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    BEDROCK_MODEL_ID: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/llmops")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    OPENSEARCH_URL: str = os.getenv("OPENSEARCH_URL", "https://localhost:9200")
    OPENSEARCH_USER: str = os.getenv("OPENSEARCH_USER", "admin")
    OPENSEARCH_PASSWORD: str = os.getenv("OPENSEARCH_PASSWORD", "admin")
    
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")

    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_PROJECT: str = "llm-ops-rag"

    class Config:
        env_file = ".env"

settings = Settings()
