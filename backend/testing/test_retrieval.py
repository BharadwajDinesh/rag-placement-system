"""
Simple test script for retrieval service
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.services.retrieval import RetrievalService


def test_retrieval():
    """Test retrieval with sample queries"""
    
    print("\n" + "="*60)
    print("Testing Retrieval Service")
    print("="*60)
    
    # Initialize
    print("\nInitializing...")
    service = RetrievalService()
    print("✅ Service ready")
    
    # Test queries
    queries = [
        "What are the eligibility criteria?",
        "Tell me about the placement process",
        "What is the placement policy?"
    ]
    
    print(f"\nTesting {len(queries)} queries...\n")
    
    for i, query in enumerate(queries, 1):
        print(f"{i}. Query: {query}")
        
        results = service.retrieve(query, top_k=2)
        
        if results:
            print(f"   ✅ Found {len(results)} results")
            for j, r in enumerate(results, 1):
                print(f"      [{j}] Score: {r.score:.3f} | {r.text[:80]}...")
        else:
            print("   ⚠️  No results")
        print()
    
    print("="*60)
    print("✅ Test complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        test_retrieval()
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
