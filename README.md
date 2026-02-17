# RAG Placement System

A **Retrieval-Augmented Generation (RAG)** system designed to answer questions about institutional placement policies using AI-powered document processing and natural language understanding.

## 🎯 Project Overview

This project implements an intelligent question-answering system that:
- **Processes PDF documents** (specifically placement policy documents)
- **Generates semantic embeddings** using HuggingFace models
- **Stores and retrieves** information using MongoDB Atlas Vector Search
- **Generates contextual answers** using Large Language Models (LLMs)
- **Provides a REST API** for querying the knowledge base

## 🏗️ Architecture

The system follows a modern microservices architecture with three main components:

```
┌─────────────┐      ┌─────────────┐      ┌──────────────┐
│  Frontend   │ ───▶ │   Backend   │ ───▶ │   MongoDB    │
│  (Vite/JS)  │      │  (FastAPI)  │      │    Atlas     │
└─────────────┘      └─────────────┘      └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ HuggingFace  │
                     │     API      │
                     └──────────────┘
```

### Core Components

#### 1. **PDF Processing Pipeline** (`pdf_processor.py`)
- Loads PDF documents using LangChain's `PyPDFLoader`
- Splits documents into semantic chunks (1000 chars with 200 char overlap)
- Generates unique chunk IDs and preserves metadata (page numbers, source)

#### 2. **Embedding Service** (`embeddings.py`)
- Uses HuggingFace Inference API for cloud-based embeddings
- Model: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- Batch processing with rate limit handling
- Converts text chunks into dense vector representations

#### 3. **Vector Store** (`vector_store.py`)
- MongoDB Atlas integration with vector search capabilities
- Cosine similarity search for semantic retrieval
- Efficient indexing and querying of high-dimensional embeddings

#### 4. **LLM Service** (`llm.py`)
- Uses `google/flan-t5-base` for answer generation
- Context-aware response generation
- Handles cases where information is not available in the knowledge base

#### 5. **FastAPI Backend** (`main.py`)
- RESTful API endpoints for document querying
- CORS-enabled for frontend integration
- Health check and query endpoints
- Lazy loading of services for optimal performance

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MongoDB Atlas account (with Vector Search enabled)
- HuggingFace API token
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/BharadwajDinesh/rag-placement-system.git
cd rag-placement-system
```

2. **Set up environment variables**

Create a `.env` file in the `backend` directory:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
MONGODB_DB_NAME=placement_rag
MONGODB_COLLECTION=documents
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=google/flan-t5-base
```

3. **Install dependencies**

```bash
cd backend
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

This will start:
- Backend API at `http://localhost:8000`
- Frontend at `http://localhost:5173`

#### Option 2: Manual Setup

**Backend:**
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📊 ETL Pipeline

The ETL (Extract, Transform, Load) pipeline processes PDF documents and populates the vector database:

```bash
cd backend
python etl.py
```

**Pipeline Steps:**
1. Load PDF from `data/` directory
2. Extract and chunk text content
3. Generate embeddings via HuggingFace API
4. Store chunks with embeddings in MongoDB Atlas

## 🔧 Configuration

Key configuration parameters in `backend/app/config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | HuggingFace embedding model |
| `LLM_MODEL` | `google/flan-t5-base` | Language model for answer generation |
| `TOP_K` | `3` | Number of similar chunks to retrieve |
| `SIMILARITY_THRESHOLD` | `0.7` | Minimum similarity score for results |
| `API_PORT` | `8000` | Backend API port |

## 📡 API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

### Query Documents
```http
POST /query
Content-Type: application/json

{
  "question": "What is the placement policy for final year students?"
}
```

**Response:**
```json
{
  "answer": "According to the placement policy...",
  "sources": [
    {
      "text": "Relevant chunk text...",
      "score": 0.89
    }
  ]
}
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **LangChain** - Framework for LLM applications
- **PyMongo** - MongoDB driver for Python
- **HuggingFace Hub** - Cloud-based model inference
- **PyTorch** - Deep learning framework
- **Pydantic** - Data validation using Python type annotations

### Frontend
- **Vite** - Next-generation frontend tooling
- **JavaScript** - Core programming language

### Database
- **MongoDB Atlas** - Cloud database with vector search capabilities

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 📁 Project Structure

```
rag-placement-system/
├── backend/
│   ├── app/
│   │   ├── api/              # API route handlers
│   │   ├── models/           # Pydantic models
│   │   ├── services/         # Core business logic
│   │   │   ├── embeddings.py
│   │   │   ├── pdf_processor.py
│   │   │   ├── vector_store.py
│   │   │   └── llm.py
│   │   ├── utils/            # Helper functions
│   │   ├── config.py         # Configuration management
│   │   └── main.py           # FastAPI application
│   ├── etl.py                # ETL pipeline script
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/                  # Frontend source code
│   ├── public/               # Static assets
│   ├── package.json
│   └── Dockerfile
├── data/                     # PDF documents for processing
├── scripts/                  # Utility scripts
├── docker-compose.yml
└── README.md
```

## 🧪 Testing

The project includes several test scripts:

- `test_embeddings.py` - Test embedding generation
- `test_connection.py` - Verify MongoDB connection
- `verify_mongo_index.py` - Check vector search index setup
- `quick_test.py` - Quick integration test

Run tests:
```bash
cd backend
python test_embeddings.py
```

## 🔍 How It Works

1. **Document Ingestion**: PDF documents are loaded and split into semantic chunks
2. **Embedding Generation**: Each chunk is converted to a 384-dimensional vector using HuggingFace's sentence transformer
3. **Vector Storage**: Embeddings are stored in MongoDB Atlas with vector search indexing
4. **Query Processing**: User questions are embedded using the same model
5. **Semantic Search**: MongoDB performs cosine similarity search to find relevant chunks
6. **Answer Generation**: Retrieved context is fed to the LLM to generate a natural language answer

## 🎓 Use Case

This system is specifically designed for **IIIT Kottayam's placement policy** but can be adapted for:
- Academic policy Q&A systems
- Corporate knowledge bases
- Legal document analysis
- Technical documentation search
- Research paper repositories

## 🔐 Security Considerations

- API keys are stored in environment variables (`.env` file)
- `.env` file is gitignored to prevent credential leakage
- Use `.env.example` as a template for required variables
- MongoDB connection uses secure URI with authentication

## 🚧 Future Enhancements

- [ ] Multi-document support
- [ ] User authentication and authorization
- [ ] Conversation history and context retention
- [ ] Advanced filtering and metadata search
- [ ] Performance monitoring and analytics
- [ ] Support for multiple file formats (DOCX, TXT, etc.)
- [ ] Fine-tuned models for domain-specific accuracy

## 📝 License

This project is developed as part of M.Tech coursework at IIIT Kottayam.

## 👥 Contributors

- **Bharadwaj Dinesh** - [GitHub](https://github.com/BharadwajDinesh)

## 🤝 Acknowledgments

- HuggingFace for providing inference APIs
- MongoDB Atlas for vector search capabilities
- LangChain for document processing utilities
- FastAPI for the excellent web framework

---

**Note**: This is an educational project demonstrating RAG architecture for intelligent document querying systems.
