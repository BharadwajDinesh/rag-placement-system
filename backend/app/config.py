from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    # MongoDB
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "placement_rag"
    MONGODB_COLLECTION: str = "documents"
    
    # HuggingFace API
    HUGGINGFACE_API_KEY: str
    
    # Models
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL: str = "google/flan-t5-base"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Vector Search
    TOP_K: int = 3
    SIMILARITY_THRESHOLD: float = 0.7
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()