"""
Retrieval Service for RAG System
Handles query processing and semantic search
"""

from typing import List, Dict, Optional
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore
from app.config import get_settings


class RetrievalResult:
    """Represents a single retrieval result"""
    def __init__(self, text: str, chunk_id: str, score: float, metadata: Dict = None):
        self.text = text
        self.chunk_id = chunk_id
        self.score = score
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "text": self.text,
            "chunk_id": self.chunk_id,
            "score": self.score,
            "metadata": self.metadata
        }


class RetrievalService:
    """Service for retrieving relevant document chunks based on queries"""
    
    def __init__(self):
        """Initialize retrieval service with embeddings and vector store"""
        settings = get_settings()
        
        # Initialize embedding service for query encoding
        self.embedding_service = EmbeddingService(
            model_name=settings.EMBEDDING_MODEL,
            api_key=settings.HUGGINGFACE_API_KEY
        )
        
        # Initialize vector store for similarity search
        self.vector_store = VectorStore(
            mongodb_uri=settings.MONGODB_URI,
            db_name=settings.MONGODB_DB_NAME,
            collection_name=settings.MONGODB_COLLECTION
        )
        
        # Default retrieval parameters
        self.default_top_k = settings.TOP_K
        self.similarity_threshold = settings.SIMILARITY_THRESHOLD
    
    def retrieve(
        self, 
        query: str, 
        top_k: Optional[int] = None,
        min_score: Optional[float] = None
    ) -> List[RetrievalResult]:
        """
        Retrieve relevant document chunks for a given query.
        
        Args:
            query: User query string
            top_k: Number of results to return (default from config)
            min_score: Minimum similarity score threshold (default from config)
            
        Returns:
            List of RetrievalResult objects sorted by relevance
        """
        # Use defaults if not specified
        top_k = top_k or self.default_top_k
        min_score = min_score or self.similarity_threshold
        
        # Step 1: Generate embedding for the query
        query_embedding = self.embedding_service.generate_single_embedding(query)
        
        # Convert numpy array to list if needed (MongoDB requires list format)
        if hasattr(query_embedding, 'tolist'):
            query_embedding = query_embedding.tolist()
        
        # Step 2: Perform vector similarity search
        raw_results = self.vector_store.search_similar(
            query_embedding=query_embedding,
            top_k=top_k
        )
        
        # Step 3: Format and filter results
        results = self._format_results(raw_results, min_score)
        
        return results
    
    def _format_results(
        self, 
        raw_results: List[Dict],
        min_score: float
    ) -> List[RetrievalResult]:
        """
        Format raw MongoDB results into RetrievalResult objects.
        
        Args:
            raw_results: Raw results from MongoDB vector search
            min_score: Minimum score threshold for filtering
            
        Returns:
            List of formatted RetrievalResult objects
        """
        formatted_results = []
        
        for result in raw_results:
            # Extract fields from MongoDB result
            text = result.get("text", "")
            chunk_id = result.get("chunk_id", "")
            score = result.get("score", 0.0)
            metadata = result.get("metadata", {})
            
            # Filter by minimum score
            if score >= min_score:
                retrieval_result = RetrievalResult(
                    text=text,
                    chunk_id=chunk_id,
                    score=score,
                    metadata=metadata
                )
                formatted_results.append(retrieval_result)
        
        return formatted_results
    
    def get_context_for_llm(
        self, 
        query: str, 
        top_k: Optional[int] = None
    ) -> str:
        """
        Retrieve and format context for LLM prompt.
        
        Args:
            query: User query string
            top_k: Number of results to retrieve
            
        Returns:
            Formatted context string ready for LLM prompt
        """
        results = self.retrieve(query, top_k)
        
        if not results:
            return "No relevant information found."
        
        # Format results as numbered context
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"[{i}] {result.text}")
        
        return "\n\n".join(context_parts)
