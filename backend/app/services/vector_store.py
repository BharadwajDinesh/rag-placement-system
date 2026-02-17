from pymongo import MongoClient
from typing import List, Dict
import numpy as np

class VectorStore:
    def __init__(self, mongodb_uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    
    def create_vector_index(self, embedding_dimension: int):
        """Create Atlas Vector Search index (run once)"""
        # This needs to be done via Atlas UI or API
        # Index definition for Atlas:
        index_definition = {
            "mappings": {
                "dynamic": True,
                "fields": {
                    "embedding": {
                        "type": "knnVector",
                        "dimensions": embedding_dimension,
                        "similarity": "cosine"
                    }
                }
            }
        }
        print("Create this index in MongoDB Atlas UI:")
        print(index_definition)
    
    def insert_documents(self, documents: List[Dict]):
        """Insert documents with embeddings"""
        if documents:
            self.collection.insert_many(documents)
    
    def search_similar(self, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
        """Vector similarity search using MongoDB Atlas"""
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",  # Name of your Atlas index
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": top_k * 10,
                    "limit": top_k
                }
            },
            {
                "$project": {
                    "text": 1,
                    "chunk_id": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        return results
    
    def clear_collection(self):
        """Clear all documents"""
        self.collection.delete_many({})