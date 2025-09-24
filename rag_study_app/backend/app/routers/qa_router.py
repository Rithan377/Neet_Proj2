# router/qa_router.py
from fastapi import APIRouter
from pydantic import BaseModel

from app.db.vector_db_instance import vector_db  # Use the shared global instance
from app.services.rag_service import retrieve_and_summarize
from app.db.vector_db import VectorDB

# Create router
router = APIRouter(tags=["Question Answering"])


class Question(BaseModel):
    query: str
    top_k: int = 1  # default to 1 result


@router.post("/")
async def ask_question(payload: Question):
    """
    Takes a query, retrieves top chunks from FAISS,
    summarizes each via LLM, and returns both raw and summarized content.
    """
    # 1. Check if vector DB is initialized
    if vector_db is None or not hasattr(vector_db, "index"):
        return {"error": "VectorDB not initialized. Run ingestion first."}

    if vector_db.index.ntotal == 0:
        return {"error": "VectorDB is empty. Run ingestion first."}

    # 2. Retrieve and summarize chunks using RAG service
    results = retrieve_and_summarize(payload.query, top_k=payload.top_k)

    # 3. Return cleaned results (embeddings already excluded)
    return {"query": payload.query, "results": results}


# --------------------------
# Optional helper (if you want to manually inject another DB)
# --------------------------
def set_vector_db(db: VectorDB):
    global vector_db
    vector_db = db
