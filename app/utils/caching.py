import redis
import json
import os
from typing import Optional, Any
from dotenv import load_dotenv

load_dotenv()

class CacheService:
    def __init__(self):
        self.redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

    def get(self, key: str) -> Optional[Any]:
        """Retrieve data from cache."""
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    def set(self, key: str, value: Any, expire: int = 3600):
        """Store data in cache with an expiration time in seconds."""
        self.redis_client.set(key, json.dumps(value), ex=expire)

    def generate_cache_key(self, query: str, agent_id: str) -> str:
        """Generate a unique cache key for a query and agent."""
        return f"cache:{agent_id}:{query.strip().lower()}"

cache_service = CacheService()
