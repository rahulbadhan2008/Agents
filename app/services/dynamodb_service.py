import boto3
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.table_name = os.getenv("DYNAMODB_AGENTS_TABLE", "AgentsMetadata")
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        try:
            self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[{'AttributeName': 'agent_id', 'KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'agent_id', 'AttributeType': 'S'}],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
        except self.dynamodb.meta.client.exceptions.ResourceInUseException:
            pass

    def save_agent(self, agent_data: Dict[str, Any]):
        table = self.dynamodb.Table(self.table_name)
        table.put_item(Item=agent_data)

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        table = self.dynamodb.Table(self.table_name)
        response = table.get_item(Key={'agent_id': agent_id})
        return response.get('Item')

    def delete_agent(self, agent_id: str):
        table = self.dynamodb.Table(self.table_name)
        table.delete_item(Key={'agent_id': agent_id})

dynamodb_service = DynamoDBService()
