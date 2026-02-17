from huggingface_hub import InferenceClient
from typing import List
import os

class EmbeddingService:
    def __init__(self, model_name: str, api_key: str = None):
        """
        Initialize embedding service using HuggingFace Inference API.
        
        Args:
            model_name: HuggingFace model ID (e.g., 'sentence-transformers/all-MiniLM-L6-v2')
            api_key: HuggingFace API token (if not provided, uses HF_TOKEN env var)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "HuggingFace API key not found. "
                "Set HUGGINGFACE_API_KEY in .env or pass api_key parameter."
            )
        
        # Initialize HuggingFace Inference Client
        self.client = InferenceClient(token=self.api_key)
        
        # Dimension for all-MiniLM-L6-v2 is 384
        # Update this if using a different model
        self.dimension = 384
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using HuggingFace API.
        
        Args:
            texts: List of strings to embed
            
        Returns:
            List of embedding vectors (each is a list of floats)
        """
        embeddings = []
        
        # Process in batches to respect API rate limits
        batch_size = 10
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            for text in batch:
                # Call HuggingFace Inference API
                embedding = self.client.feature_extraction(
                    text=text,
                    model=self.model_name
                )
                embeddings.append(embedding)
        
        return embeddings
    
    def generate_single_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text using HuggingFace API.
        
        Args:
            text: String to embed
            
        Returns:
            Embedding vector as a list of floats
        """
        embedding = self.client.feature_extraction(
            text=text,
            model=self.model_name
        )
        return embedding