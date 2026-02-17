"""
Quick inline test - Run this to test embeddings immediately
Works with both system environment variables and .env file
"""

import os
import sys
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

# Check if API key exists
api_key = os.getenv("HUGGINGFACE_API_KEY")

if not api_key:
    print("[X] HUGGINGFACE_API_KEY not found in .env file!")
    print("\nPlease:")
    print("1. Get your API key from https://huggingface.co/settings/tokens")
    print("2. Add it to your .env file: HUGGINGFACE_API_KEY=hf_your_token_here")
    exit(1)

print(f"[OK] API Key found: {api_key[:10]}...")

# Test the embedding service
print("\nTesting HuggingFace API...")

from huggingface_hub import InferenceClient

try:
    client = InferenceClient(token=api_key)
    
    # Test with a simple text
    test_text = "Hello, this is a test!"
    print(f"\nGenerating embedding for: '{test_text}'")
    
    embedding = client.feature_extraction(
        text=test_text,
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    print(f"\n[SUCCESS!]")
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
    print(f"\n[DONE] Your HuggingFace API is working correctly!")
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    print("\nPossible issues:")
    print("1. Invalid API key")
    print("2. No internet connection")
    print("3. API rate limit exceeded")
