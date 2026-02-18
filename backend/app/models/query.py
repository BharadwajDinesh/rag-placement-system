"""
Pydantic models for query API requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class QueryRequest(BaseModel):
    """Request model for query endpoint"""
    query: str = Field(..., description="User query text", min_length=1)
    top_k: Optional[int] = Field(3, description="Number of results to return", ge=1, le=10)
    min_score: Optional[float] = Field(None, description="Minimum similarity score threshold", ge=0.0, le=1.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the eligibility criteria for placements?",
                "top_k": 3,
                "min_score": 0.7
            }
        }


class RetrievalResultModel(BaseModel):
    """Model for a single retrieval result"""
    text: str = Field(..., description="Retrieved text chunk")
    chunk_id: str = Field(..., description="Unique chunk identifier")
    score: float = Field(..., description="Similarity score (0-1, higher is better)")
    metadata: Dict = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Students must have a minimum CGPA of 7.0 to be eligible for placements.",
                "chunk_id": "chunk_001",
                "score": 0.89,
                "metadata": {"page": 3, "section": "Eligibility"}
            }
        }


class QueryResponse(BaseModel):
    """Response model for query endpoint"""
    query: str = Field(..., description="Original query text")
    results: List[RetrievalResultModel] = Field(..., description="List of retrieved results")
    total_results: int = Field(..., description="Total number of results returned")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the eligibility criteria for placements?",
                "results": [
                    {
                        "text": "Students must have a minimum CGPA of 7.0 to be eligible for placements.",
                        "chunk_id": "chunk_001",
                        "score": 0.89,
                        "metadata": {"page": 3}
                    }
                ],
                "total_results": 1
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
    services: Dict[str, str] = Field(default_factory=dict, description="Individual service statuses")


class ChatRequest(BaseModel):
    """Request model for RAG chat endpoint"""
    query: str = Field(..., description="User question", min_length=1)
    top_k: Optional[int] = Field(3, description="Number of chunks to retrieve", ge=1, le=10)

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the One Student One Job policy?",
                "top_k": 3
            }
        }


class SourceChunk(BaseModel):
    """A source chunk used to generate the answer"""
    chunk_id: str
    score: float
    text_preview: str


class ChatResponse(BaseModel):
    """Response model for RAG chat endpoint"""
    query: str = Field(..., description="Original user question")
    answer: str = Field(..., description="Generated answer from FLAN-T5")
    sources: List[SourceChunk] = Field(..., description="Source chunks used to generate the answer")
