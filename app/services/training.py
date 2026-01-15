import boto3
import os
from sqlalchemy.orm import Session
from ..models.models import Memory, MemoryTier
import json

class TrainingService:
    def __init__(self, db: Session):
        self.db = db
        self.bedrock = boto3.client("bedrock", region_name=os.getenv("AWS_REGION", "us-east-1"))

    def prepare_fine_tuning_data(self):
        # Fetch long-term memories for fine-tuning
        memories = self.db.query(Memory).filter(Memory.tier == MemoryTier.LONG_TERM).all()
        
        formatted_data = []
        for mem in memories:
            content = mem.content
            formatted_data.append({
                "prompt": content.get("query"),
                "completion": content.get("response")
            })
            
        # Write to S3 or local file for training
        with open("fine_tuning_data.jsonl", "w") as f:
            for item in formatted_data:
                f.write(json.dumps(item) + "\n")
        
        return "fine_tuning_data.jsonl"

    def start_fine_tuning(self, job_name: str, base_model_id: str):
        # This is a simplified call to Bedrock fine-tuning API
        response = self.bedrock.create_model_customization_job(
            jobName=job_name,
            customModelName=f"{job_name}-custom",
            roleArn="your_iam_role_arn",
            baseModelIdentifier=base_model_id,
            trainingDataConfig={"s3Uri": "s3://your-bucket/fine_tuning_data.jsonl"},
            outputDataConfig={"s3Uri": "s3://your-bucket/output/"}
        )
        return response["jobArn"]

def get_training_service(db: Session):
    return TrainingService(db)
