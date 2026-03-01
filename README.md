# NEET RAG Study App

NEET RAG Study App is a **Retrieval-Augmented Generation (RAG)** based study assistant designed to help users query and learn from medical study material efficiently. The system combines document ingestion, vector search, and LLM-based question answering to provide **context-aware, grounded responses** from uploaded study content.

The project is structured as a **full-stack application** with a Python-based backend and a frontend layer, following clean modular design principles.

---

![Python](https://img.shields.io/badge/python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-backend-009688?style=flat&logo=fastapi&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-vector%20database-0467DF?style=flat)
![RAG](https://img.shields.io/badge/RAG-retrieval--augmented--generation-6A5ACD?style=flat)
![Gemini](https://img.shields.io/badge/Gemini-Google%20LLM-4285F4?style=flat&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/docker-containerized-2496ED?style=flat&logo=docker&logoColor=white)
![ngrok](https://img.shields.io/badge/ngrok-api%20exposure-1F1E37?style=flat&logo=ngrok&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-yellow?style=flat)

## Project Overview

The application allows users to:

- Ingest study material (PDFs)
- Convert content into vector embeddings
- Store and search embeddings using FAISS
- Answer questions using a Retrieval-Augmented Generation pipeline
- Serve responses through a FastAPI backend

The architecture is optimized for **clarity, extensibility, and real-world RAG workflows**, rather than simple prompt-based demos.

---


## High-Level Architecture

1. **Document Ingestion**
   - PDFs are parsed and chunked
   - Chunks are embedded using a sentence-transformer model

2. **Vector Storage**
   - Embeddings are stored in a FAISS index
   - Index is persisted and reused across restarts

3. **Query Flow**
   - User query is embedded
   - Relevant chunks are retrieved from FAISS
   - Retrieved context is passed to an LLM for answer generation

4. **API Layer**
   - FastAPI exposes endpoints for querying and testing
   - Modular routers handle different resources

---

## Tech Stack

### Backend
- Python 3.10
- FastAPI
- FAISS (vector database)
- Sentence Transformers (`all-MiniLM-L6-v2`)
- NumPy (pinned to `< 2.0`)
- Uvicorn
- Docker (optional)

### Frontend
- Node.js (package scaffold present)

### Data
- PDF-based study material
- Vector index persisted to disk

---

## Project Structure

```
Neet_Proj2/
├── rag_study_app/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── main.py              # FastAPI entry point
│   │   │   ├── config.py            # App configuration
│   │   │   ├── routers/             # API route definitions
│   │   │   ├── services/            # RAG, embedding, QA logic
│   │   │   ├── db/                  # FAISS vector DB logic
│   │   │   ├── scripts/             # Utility and setup scripts
│   │   │   └── utils/               # Helper utilities
│   │   ├── requirements.txt         # Backend dependencies
│   │   ├── Dockerfile               # Backend container setup
│   │   ├── start.sh                 # Startup script
│   │   ├── faiss.index              # Persisted FAISS index
│   │   └── faiss.index.chunks       # Index metadata
│   ├── data/
│   │   └── med-test-rag.pdf          # Sample study material
│   ├── frontend/
│   │   └── package.json             # Frontend scaffold
│   └── tests/
│       ├── test_embedding.py
│       ├── test_parser.py
│       └── test_qa.py
├── setup/
│   ├── folder.py
│   └── req.txt
└── README.md
```


---
---

## Architecture & Workflow

### RAG Stream Flow (Development)

![RAG Stream Flow](assets/stream_flow.png)

### System Architecture

![System Architecture](assets/image.png)
![System Architecture – Alternate View](assets/image_copy.png)

## Requirements

- Python 3.10
- pip
- Virtual environment (recommended)
- FAISS-compatible CPU
- Internet access (for model downloads on first run)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Rithan377/Neet_Proj2.git
cd Neet_Proj2

Create and activate virtual environment
python3.10 -m venv venv
source venv/bin/activate

Install backend dependencies
cd rag_study_app/backend
pip install -r requirements.txt

Run the Backend Server

From the backend directory:

uvicorn app.main:app --reload

The server will start at:

http://127.0.0.1:8000

API Usage

Once running, visit:

http://127.0.0.1:8000/docs

This provides interactive Swagger documentation for testing endpoints.

Testing

Run tests from the rag_study_app directory:

pytest tests/  

Author
Rithan
GitHub: https://github.com/Rithan377


