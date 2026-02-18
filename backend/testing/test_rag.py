"""
Simple test for the full RAG pipeline (retrieval + Groq Llama 3)
"""

import sys
import io
from pathlib import Path

# Fix Windows terminal Unicode encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))

from app.services.rag_pipeline import RAGPipeline


def test_rag():
    print("\n" + "="*60)
    print("Testing RAG Pipeline (Retrieval + Groq Llama 3)")
    print("="*60)

    print("\nInitializing RAG pipeline...")
    pipeline = RAGPipeline()
    print("Pipeline ready")

    queries = [
        "What is the One Student One Job policy?",
        "What are the eligibility criteria for placements?",
        "What is the role of the Training and Placement Cell?"
    ]

    print(f"\nTesting {len(queries)} queries...\n")

    for i, query in enumerate(queries, 1):
        print(f"{i}. Query: {query}")
        result = pipeline.answer(query, top_k=3)
        print(f"   Answer: {result.answer}")
        print(f"   Sources used: {len(result.sources)}")
        for s in result.sources:
            print(f"      - Score: {s['score']:.3f} | {s['text_preview'][:60]}...")
        print()

    print("="*60)
    print("RAG pipeline test complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        test_rag()
    except Exception as e:
        print(f"\nError: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
