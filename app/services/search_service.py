from opensearchpy import OpenSearch
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

class SearchService:
    def __init__(self):
        # OpenSearch Setup
        self.os_client = OpenSearch(
            hosts=[os.getenv("OPENSEARCH_URL", "https://localhost:9200")],
            http_auth=(os.getenv("OPENSEARCH_USER", "admin"), os.getenv("OPENSEARCH_PASSWORD", "admin")),
            use_ssl=True,
            verify_certs=False,
            ssl_show_warn=False
        )
        
        # Neo4j Setup
        self.neo4j_driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
        )

    def hybrid_search(self, query: str, vector: list = None, top_k: int = 5):
        # 1. OpenSearch Keyword Search (BM25)
        bm25_query = {
            "size": top_k,
            "query": {
                "match": {
                    "text": query
                }
            }
        }
        bm25_results = self.os_client.search(index="docs", body=bm25_query)

        # 2. OpenSearch Vector Search (Semantic)
        vector_results = []
        if vector:
            knn_query = {
                "size": top_k,
                "query": {
                    "knn": {
                        "embedding": {
                            "vector": vector,
                            "k": top_k
                        }
                    }
                }
            }
            vector_results = self.os_client.search(index="docs", body=knn_query)

        # 3. Neo4j Graph Search (Relationships)
        graph_results = self.get_graph_context(query)

        return {
            "bm25": bm25_results,
            "vector": vector_results,
            "graph": graph_results
        }

    def get_graph_context(self, query: str):
        with self.neo4j_driver.session() as session:
            # Simple example: find nodes related to the query terms
            result = session.run(
                "MATCH (n)-[r]->(m) WHERE n.name CONTAINS $query OR m.name CONTAINS $query RETURN n, r, m LIMIT 5",
                query=query
            )
            return [record.data() for record in result]

    def close(self):
        self.neo4j_driver.close()

search_service = SearchService()
