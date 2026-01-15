import json
import os
import sys

# Add app directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal
from app.models.models import Memory, MemoryTier

def generate_fine_tuning_jsonl(output_path: str = "fine_tuning_data.jsonl"):
    """
    Simulate data accumulation by fetching long-term memories 
    and formatting them for AWS Bedrock fine-tuning.
    """
    db = SessionLocal()
    try:
        # Fetch long-term memories
        memories = db.query(Memory).filter(Memory.tier == MemoryTier.LONG_TERM).all()
        
        if not memories:
            print("No long-term memories found. Generating dummy data for demonstration.")
            # Dummy data for demonstration
            memories = [
                type('obj', (object,), {"content": {"query": "How do I setup ECS?", "response": "Use AWS CodePipeline for automated deployment to ECS clusters."}})(),
                type('obj', (object,), {"content": {"query": "What is the benefit of hybrid search?", "response": "Hybrid search combines BM25 keyword matching with vector embeddings for better recall."}})()
            ]

        with open(output_path, "w") as f:
            for mem in memories:
                data = {
                    "prompt": mem.content.get("query"),
                    "completion": mem.content.get("response")
                }
                f.write(json.dumps(data) + "\n")
        
        print(f"Successfully generated fine-tuning data at: {output_path}")
        return output_path
    finally:
        db.close()

if __name__ == "__main__":
    generate_fine_tuning_jsonl()
