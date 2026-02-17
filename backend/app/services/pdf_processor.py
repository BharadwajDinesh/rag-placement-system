from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict
import hashlib

class PDFProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize PDF processor with LangChain components.
        
        Args:
            chunk_size: Maximum size of each text chunk (in characters, not words)
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]  # Try to split on semantic boundaries
        )


    
    def process_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Main processing pipeline: load PDF and split into chunks.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing chunked documents with metadata
        """
        # Load PDF using LangChain
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        # Split documents into chunks
        split_docs = self.text_splitter.split_documents(documents)
        
        # Convert to our format
        chunks = []
        for idx, doc in enumerate(split_docs):
            chunk_id = hashlib.md5(doc.page_content.encode()).hexdigest()
            chunks.append({
                "chunk_id": chunk_id,
                "text": doc.page_content,
                "chunk_index": idx,
                "metadata": {
                    "source": pdf_path,
                    "page": doc.metadata.get("page", None)
                }
            })
        
        return chunks