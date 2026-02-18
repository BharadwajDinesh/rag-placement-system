"""
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.query import router as query_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Placement Policy RAG API",
    description="RAG system for querying IIIT Kota placement policies using Groq Llama 3.3",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router)


@app.get("/")
async def root():
    return {
        "message": "Placement Policy RAG API",
        "endpoints": {
            "health": "/api/health",
            "search": "POST /api/query",
            "chat": "POST /api/chat",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)