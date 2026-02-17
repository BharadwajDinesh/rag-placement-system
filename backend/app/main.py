from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn

from app.config import get_settings
from app.services.pdf_processor import PDFProcessor
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.llm import LLMService

app = FastAPI(title="Placement Policy RAG API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()

# Initialize services (lazy loading)
_embedding_service = None
_vector_store = None
_llm_service = None

def get_embedding_service():
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService(
            settings.EMBEDDING_MODEL,
            settings.HUGGINGFACE_API_KEY
        )
    return _embedding_service

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore(
            settings.MONGODB_URI,
            settings.MONGODB_DB_NAME,
            settings.MONGODB_COLLECTION
        )
    return _vector_store

def get_llm_service():
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService(settings.LLM_MODEL)
    return _llm_service

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict]

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        # Generate query embedding
        embedding_service = get_embedding_service()
        query_embedding = embedding_service.generate_single_embedding(request.question)
        
        # Search similar documents
        vector_store = get_vector_store()
        results = vector_store.search_similar(query_embedding, top_k=settings.TOP_K)
        
        if not results:
            raise HTTPException(status_code=404, detail="No relevant information found")
        
        # Prepare context
        context = "\n\n".join([doc["text"] for doc in results])
        
        # Generate answer
        llm_service = get_llm_service()
        answer = llm_service.generate_answer(request.question, context)
        
        return QueryResponse(
            answer=answer,
            sources=[{"text": doc["text"][:200], "score": doc["score"]} for doc in results]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)