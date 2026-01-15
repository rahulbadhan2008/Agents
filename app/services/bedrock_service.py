from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks.tracers import LangChainTracer
import os
from dotenv import load_dotenv

load_dotenv()

class BedrockService:
    def __init__(self):
        self.model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
        self.client = ChatBedrock(
            model_id=self.model_id,
            model_kwargs={"temperature": 0.05} # Based on user's 'p.05' request
        )
        # LangSmith endpoint is handled by environment variables
        
    def generate_response(self, system_prompt: str, user_query: str, chat_history: list = None):
        messages = [
            SystemMessage(content=system_prompt),
        ]
        
        if chat_history:
            messages.extend(chat_history)
            
        messages.append(HumanMessage(content=user_query))
        
        response = self.client.invoke(messages)
        return response.content

    def get_llm(self):
        return self.client

bedrock_service = BedrockService()
