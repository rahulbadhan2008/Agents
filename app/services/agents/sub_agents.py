from .bedrock_service import bedrock_service
from langchain_core.messages import HumanMessage
import json

class SubAgent:
    def __init__(self, role: str):
        self.role = role
        self.llm = bedrock_service.get_llm()

    def run(self, input_data: dict):
        pass

class RetrievalAgent(SubAgent):
    def __init__(self):
        super().__init__("retrieval")

    def plan_queries(self, query: str):
        prompt = f"Generate 3 optimized search queries for: {query}"
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content.split("\n")

class RerankingAgent(SubAgent):
    def __init__(self):
        super().__init__("reranking")

    def rerank(self, query: str, documents: list):
        # In a real scenario, this would use a Cross-Encoder or a specialized LLM call
        prompt = f"Rerank these documents based on relevance to '{query}':\n{json.dumps(documents)}"
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content

class SynthesisAgent(SubAgent):
    def __init__(self):
        super().__init__("synthesis")

    def synthesize(self, query: str, context: str):
        prompt = f"Synthesize a final answer for '{query}' using the context:\n{context}"
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
