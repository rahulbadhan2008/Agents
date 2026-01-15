import boto3
import logging
import time
import os
from dotenv import load_dotenv

load_dotenv()

class CloudWatchLogger:
    def __init__(self, log_group="LLMOpsLogs", log_stream="RAGApp"):
        self.client = boto3.client("logs", region_name=os.getenv("AWS_REGION", "us-east-1"))
        self.log_group = log_group
        self.log_stream = log_stream
        self._ensure_log_group_and_stream()

    def _ensure_log_group_and_stream(self):
        try:
            self.client.create_log_group(logGroupName=self.log_group)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass
        
        try:
            self.client.create_log_stream(logGroupName=self.log_group, logStreamName=self.log_stream)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass

    def log(self, message: str, level: str = "INFO"):
        self.client.put_log_events(
            logGroupName=self.log_group,
            logStreamName=self.log_stream,
            logEvents=[
                {
                    'timestamp': int(round(time.time() * 1000)),
                    'message': f"[{level}] {message}"
                },
            ]
        )

cloudwatch_logger = CloudWatchLogger()
