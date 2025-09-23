import os

# =========================
# Production-ready content
# =========================

MAIN_PY = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import book_router, chapter_router, subtopic_router, qa_router

app = FastAPI(title="RAG Study App", version="1.0")

# Enable CORS for Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(book_router.router, prefix="/books")
app.include_router(chapter_router.router, prefix="/chapters")
app.include_router(subtopic_router.router, prefix="/subtopics")
app.include_router(qa_router.router, prefix="/ask")

@app.get("/")
def root():
    return {"message": "RAG Study App Backend Running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
"""

REQUIREMENTS_TXT = """fastapi==0.111.1
uvicorn[standard]==0.23.2
pydantic==2.7.0
python-multipart>=0.0.7
requests>=2.31.0
pymongo
faiss-cpu==1.7.4
torch>=2.0.0
transformers>=4.35.0
sentence-transformers>=2.2.2
python-dotenv>=1.0.1
rich>=13.6.0
gunicorn>=22.1.0
"""

DOCKERFILE = """FROM python:3.10-slim
WORKDIR /app
COPY setup/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000", "--timeout", "120"]
"""

START_SH = """#!/bin/bash
source .venv/bin/activate
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app \\
    --bind 0.0.0.0:8000 \\
    --timeout 120
"""

CONFIG_PY = """import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_index")
"""

ROUTER_PLACEHOLDERS = {
    "book_router.py": """from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_books():
    return ["NCERT Biology", "NEET Notes"]
""",
    "chapter_router.py": """from fastapi import APIRouter

router = APIRouter()

@router.get("/{book_id}")
def get_chapters(book_id: str):
    return ["Chapter 1: Human Anatomy", "Chapter 2: Plant Physiology"]
""",
    "subtopic_router.py": """from fastapi import APIRouter

router = APIRouter()

@router.get("/{chapter_id}")
def get_subtopics(chapter_id: str):
    return ["9.1 Heart", "9.2 Brain", "9.3 Lungs"]
""",
    "qa_router.py": """from fastapi import APIRouter, Body

router = APIRouter()

@router.post("/")
def ask_question(query: dict = Body(...)):
    question = query.get('question', '')
    return {"answer": f"LLM summary for: {question}"}
"""
}

INIT_PY = ""

# =========================
# New production-ready project structure
# =========================

production_structure = {
    "rag_study_app": {
        "backend": {
            "app": {
                "__init__.py": INIT_PY,
                "main.py": MAIN_PY,
                "routers": {
                    "__init__.py": INIT_PY,
                    "book_router.py": ROUTER_PLACEHOLDERS["book_router.py"],
                    "chapter_router.py": ROUTER_PLACEHOLDERS["chapter_router.py"],
                    "subtopic_router.py": ROUTER_PLACEHOLDERS["subtopic_router.py"],
                    "qa_router.py": ROUTER_PLACEHOLDERS["qa_router.py"],
                },
                "services": {
                    "__init__.py": INIT_PY,
                    "parser.py": "",
                    "embedding_service.py": "",
                    "summarizer.py": "",
                    "rag_service.py": ""
                },
                "db": {
                    "__init__.py": INIT_PY,
                    "concept_db.py": "",
                    "vector_db.py": ""
                },
                "utils": {
                    "__init__.py": INIT_PY,
                    "text_utils.py": "",
                    "caching.py": ""
                },
                "config.py": CONFIG_PY,
            },
            "requirements.txt": REQUIREMENTS_TXT,
            "Dockerfile": DOCKERFILE,
            "start.sh": START_SH
        },
        "data": {},
        "notebooks": {},
        "frontend": {
            "src": {
                "components": {},
                "pages": {},
                "services": {}
            },
            "package.json": ""
        },
        "tests": {
            "test_parser.py": "",
            "test_embedding.py": "",
            "test_qa.py": ""
        },
        "docs": {}
    }
}

# =========================
# Helper functions
# =========================

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def make_executable(path):
    os.chmod(path, 0o755)

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            write_file(path, content)
            if name == "start.sh":
                make_executable(path)

# =========================
# Run script
# =========================

if __name__ == "__main__":
    create_structure(".", production_structure)
    print("Production-ready project structure created successfully!")
