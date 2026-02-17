import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from backend.app.config import get_settings
from backend.app.services.pdf_processor import PDFProcessor
from backend.app.services.embeddings import EmbeddingService
from backend.app.services.vector_store import VectorStore
from tqdm import tqdm

def ingest_pdf(pdf_path: str):
    settings = get_settings()
    
    print("1. Processing PDF...")
    processor = PDFProcessor()
    chunks = processor.process_pdf(pdf_path)
    print(f"   Created {len(chunks)} chunks")
    
    print("2. Generating embeddings...")
    embedding_service = EmbeddingService(settings.EMBEDDING_MODEL)
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedding_service.generate_embeddings(texts)
    
    print("3. Storing in MongoDB...")
    vector_store = VectorStore(
        settings.MONGODB_URI,
        settings.MONGODB_DB_NAME,
        settings.MONGODB_COLLECTION
    )
    
    # Combine chunks with embeddings
    documents = []
    for chunk, embedding in zip(chunks, embeddings):
        doc = {
            **chunk,
            "embedding": embedding
        }
        documents.append(doc)
    
    vector_store.insert_documents(documents)
    print("✓ Ingestion complete!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/ingest_pdf.py <path_to_pdf>")
        sys.exit(1)
    
    ingest_pdf(sys.argv[1])