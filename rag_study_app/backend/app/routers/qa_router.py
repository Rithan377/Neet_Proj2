# router/qa_ro.py
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import get_embeddings
from app.db.vector_db_instance import vector_db  # Use the shared global instance
from app.db.vector_db import VectorDB

# Create router
router = APIRouter(tags=["Question Answering"])


class Question(BaseModel):
    query: str
    top_k: int = 1  # default to 3 results


@router.post("/")
async def ask_question(payload: Question):
    """
    Takes a query, embeds it, retrieves top chunks from FAISS,
    and returns them without embeddings.
    """
    # 1. Check if vector DB is initialized
    if vector_db is None or not hasattr(vector_db, "index"):
        return {"error": "VectorDB not initialized. Run ingestion first."}

    # DEBUG: Check if index is populated
    print("VectorDB total vectors:", vector_db.index.ntotal)
    if vector_db.index.ntotal == 0:
        print("VectorDB is empty! Did you forget to ingest/load vectors?")

    # 2. Embed the query
    query_emb = get_embeddings([{"text": payload.query}])[0]["embedding"]

    # 3. Search in FAISS
    results = vector_db.query(query_emb, top_k=payload.top_k)

    # 4. Remove embeddings from results
    results_clean = [
        {k: v for k, v in r.items() if k != "embedding"} for r in results
    ]

    # 5. Return cleaned chunks
    return {"query": payload.query, "results": results_clean}


# --------------------------
# Optional helper (if you want to manually inject another DB)
# --------------------------
def set_vector_db(db: VectorDB):
    global vector_db
    vector_db = db
