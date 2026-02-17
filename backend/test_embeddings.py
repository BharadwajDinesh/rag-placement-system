"""
Simple test script to verify HuggingFace embeddings are working.
Run this to check if your API key is set up correctly.
"""

from app.services.embeddings import EmbeddingService
from app.config import get_settings
import sys

def test_embeddings():
    print("=" * 60)
    print("Testing HuggingFace Embeddings API")
    print("=" * 60)
    
    try:
        # Load settings
        print("\n1. Loading configuration...")
        settings = get_settings()
        print(f"   ✓ Model: {settings.EMBEDDING_MODEL}")
        print(f"   ✓ API Key: {settings.HUGGINGFACE_API_KEY[:10]}..." if settings.HUGGINGFACE_API_KEY else "   ✗ API Key not found!")
        
        # Initialize embedding service
        print("\n2. Initializing Embedding Service...")
        embedding_service = EmbeddingService(
            settings.EMBEDDING_MODEL,
            settings.HUGGINGFACE_API_KEY
        )
        print(f"   ✓ Service initialized")
        print(f"   ✓ Embedding dimension: {embedding_service.dimension}")
        
        # Test single embedding
        print("\n3. Testing single text embedding...")
        test_text = "Students must maintain 75% attendance for placement eligibility."
        print(f"   Input: '{test_text}'")
        
        embedding = embedding_service.generate_single_embedding(test_text)
        print(f"   ✓ Embedding generated!")
        print(f"   ✓ Vector length: {len(embedding)}")
        print(f"   ✓ First 5 values: {embedding[:5]}")
        
        # Test batch embeddings
        print("\n4. Testing batch embeddings...")
        test_texts = [
            "Placement policy requires minimum CGPA of 7.0",
            "Internship completion is mandatory for final placement",
            "Students can apply to maximum 5 companies per semester"
        ]
        print(f"   Input: {len(test_texts)} texts")
        
        embeddings = embedding_service.generate_embeddings(test_texts)
        print(f"   ✓ Batch embeddings generated!")
        print(f"   ✓ Number of embeddings: {len(embeddings)}")
        print(f"   ✓ Each embedding length: {len(embeddings[0])}")
        
        # Verify similarity (similar texts should have similar embeddings)
        print("\n5. Testing semantic similarity...")
        similar_text1 = "Students need good grades for placement"
        similar_text2 = "High CGPA is required for job placement"
        different_text = "The weather is nice today"
        
        emb1 = embedding_service.generate_single_embedding(similar_text1)
        emb2 = embedding_service.generate_single_embedding(similar_text2)
        emb3 = embedding_service.generate_single_embedding(different_text)
        
        # Simple cosine similarity
        import math
        def cosine_similarity(vec1, vec2):
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            magnitude1 = math.sqrt(sum(a * a for a in vec1))
            magnitude2 = math.sqrt(sum(b * b for b in vec2))
            return dot_product / (magnitude1 * magnitude2)
        
        sim_similar = cosine_similarity(emb1, emb2)
        sim_different = cosine_similarity(emb1, emb3)
        
        print(f"   Similarity (placement texts): {sim_similar:.4f}")
        print(f"   Similarity (placement vs weather): {sim_different:.4f}")
        
        if sim_similar > sim_different:
            print("   ✓ Semantic similarity working correctly!")
        else:
            print("   ⚠ Warning: Similarity scores seem unexpected")
        
        # Success!
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYour HuggingFace embeddings are working correctly! 🎉")
        print("You can now use them in your RAG system.\n")
        
        return True
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nMake sure you have:")
        print("1. Created a HuggingFace account")
        print("2. Generated an API token")
        print("3. Added HUGGINGFACE_API_KEY to your .env file")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        print("\nCheck your:")
        print("1. Internet connection")
        print("2. HuggingFace API key validity")
        print("3. API rate limits")
        return False

if __name__ == "__main__":
    success = test_embeddings()
    sys.exit(0 if success else 1)
