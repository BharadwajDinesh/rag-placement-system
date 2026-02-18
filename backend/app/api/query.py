"""
Query API endpoints for semantic search and RAG chat
"""

from fastapi import APIRouter, HTTPException, status
from app.models.query import (
    QueryRequest, QueryResponse, RetrievalResultModel, HealthResponse,
    ChatRequest, ChatResponse, SourceChunk
)
from app.services.retrieval import RetrievalService
from app.services.rag_pipeline import RAGPipeline
from typing import List

router = APIRouter(prefix="/api", tags=["query"])

# Singleton instances
_retrieval_service = None
_rag_pipeline = None


def get_retrieval_service() -> RetrievalService:
    global _retrieval_service
    if _retrieval_service is None:
        _retrieval_service = RetrievalService()
    return _retrieval_service


def get_rag_pipeline() -> RAGPipeline:
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
    return _rag_pipeline


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Perform semantic search on document collection.
    
    Args:
        request: QueryRequest with query text and optional parameters
        
    Returns:
        QueryResponse with retrieved document chunks and scores
        
    Raises:
        HTTPException: If query processing fails
    """
    try:
        # Get retrieval service
        service = get_retrieval_service()
        
        # Perform retrieval
        results = service.retrieve(
            query=request.query,
            top_k=request.top_k,
            min_score=request.min_score
        )
        
        # Convert to response models
        result_models = [
            RetrievalResultModel(
                text=r.text,
                chunk_id=r.chunk_id,
                score=r.score,
                metadata=r.metadata
            )
            for r in results
        ]
        
        # Build response
        response = QueryResponse(
            query=request.query,
            results=result_models,
            total_results=len(result_models)
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query processing failed: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify services are ready.
    
    Returns:
        HealthResponse with service status
    """
    try:
        # Try to initialize retrieval service
        service = get_retrieval_service()
        
        return HealthResponse(
            status="healthy",
            message="All services operational",
            services={
                "retrieval": "ready",
                "embeddings": "ready",
                "vector_store": "ready"
            }
        )
        
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            message=f"Service initialization failed: {str(e)}",
            services={
                "retrieval": "error",
                "embeddings": "unknown",
                "vector_store": "unknown"
            }
        )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Full RAG pipeline: retrieve relevant chunks + generate answer with FLAN-T5.
    """
    try:
        pipeline = get_rag_pipeline()
        result = pipeline.answer(query=request.query, top_k=request.top_k)

        return ChatResponse(
            query=result.query,
            answer=result.answer,
            sources=[
                SourceChunk(
                    chunk_id=s["chunk_id"],
                    score=s["score"],
                    text_preview=s["text_preview"]
                )
                for s in result.sources
            ]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )
