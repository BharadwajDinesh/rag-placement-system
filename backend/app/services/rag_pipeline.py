"""
RAG Pipeline Service — combines retrieval + LLM generation
"""

from typing import List, Dict, Optional
from app.services.retrieval import RetrievalService, RetrievalResult
from app.services.llm import LLMService
from app.config import get_settings


class RAGResponse:
    def __init__(self, answer: str, sources: List[Dict], query: str):
        self.answer = answer
        self.sources = sources
        self.query = query


class RAGPipeline:
    def __init__(self):
        settings = get_settings()
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService(
            model_name=settings.LLM_MODEL,
            api_key=settings.GROQ_API_KEY
        )

    def answer(
        self,
        query: str,
        top_k: int = 3,
        min_score: Optional[float] = None
    ) -> RAGResponse:
        """
        Full RAG pipeline:
        1. Retrieve relevant chunks
        2. Build context
        3. Generate answer with FLAN-T5
        4. Return answer + sources
        """

        # Step 1: Retrieve
        results: List[RetrievalResult] = self.retrieval_service.retrieve(
            query=query,
            top_k=top_k,
            min_score=min_score
        )

        if not results:
            return RAGResponse(
                answer="I couldn't find relevant information to answer your question.",
                sources=[],
                query=query
            )

        # Step 2: Build context
        context = "\n\n".join(
            f"[{i+1}] {r.text}" for i, r in enumerate(results)
        )

        # Step 3: Generate answer
        answer = self.llm_service.generate_answer(query=query, context=context)

        # Step 4: Build sources list
        sources = [
            {
                "chunk_id": r.chunk_id,
                "score": round(r.score, 4),
                "text_preview": r.text[:200]
            }
            for r in results
        ]

        return RAGResponse(answer=answer, sources=sources, query=query)
