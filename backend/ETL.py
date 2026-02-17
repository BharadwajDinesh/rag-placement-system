import os
import sys
from pathlib import Path

from app.services.pdf_processor import PDFProcessor
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore
from app.config import get_settings

def process_pdf_pipeline():
    
    settings = get_settings()

    pdf_processor = PDFProcessor()
    embedding_service = EmbeddingService(
        settings.EMBEDDING_MODEL,
        settings.HUGGINGFACE_API_KEY)
    vector_store = VectorStore(
        settings.MONGODB_URI,
        settings.MONGODB_DB_NAME, 
        settings.MONGODB_COLLECTION)

    pdf_file = Path("data/Institute_Placement_Policy-IIITK_2025.pdf")

    # Generate Chunks
    chunkS = pdf_processor.process_pdf(str(pdf_file))
    
    # Generate Embeddings
    texts = [chunk["text"] for chunk in chunkS]
        # print(texts[:1])
    embeddings = embedding_service.generate_embeddings(texts)
        # print(embeddings)

    # Create document with embeddings
    documents = []
    for chunk, embedding in zip(chunkS, embeddings):
        doc = {
            "text": chunk["text"],
            "chunk_id": chunk["chunk_id"],
            "chunk_index": chunk["chunk_index"],
            "embedding": embedding.tolist() if hasattr(embedding, 'tolist') else embedding,
            "metadata": chunk.get("metadata", {})
        }
        documents.append(doc)
        # print(documents)

    # Store to MangoDB
    vector_store.insert_documents(documents)
    print(f"✅ Stored {len(documents)} documents in MongoDB!")

    
    

process_pdf_pipeline()