# app/services/rag_service.py
from typing import List
from app.db.vector_db_instance import vector_db
from app.services.embedding_service import get_embeddings

# Gemini AI SDK
import google.generativeai as genai

# ------------------------------
# Directly configure Gemini API
# ------------------------------
API_KEY = "AIzaSyD8y5OgUjK4NdBuzddahtEAKiRcDdJm4bM"  # <-- hardcoded
genai.configure(api_key=API_KEY)

# Load Gemini model
MODEL_NAME = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# ------------------------------
# Query Gemini LLM for summary
# ------------------------------
def query_llm(prompt: str) -> str:
    """
    Sends the prompt to Gemini 2.5 Flash and returns a summary.
    Truncates long text to prevent exceeding token limits.
    """
    try:
        truncated_prompt = prompt[:3000]  # keep safe within limits
        response = model.generate_content(truncated_prompt)
        return response.text or "Summary unavailable"
    except Exception as e:
        print("Gemini API error:", e)
        return "Summary unavailable due to API error"

# ------------------------------
# RAG retrieval and summarization
# ------------------------------
def retrieve_and_summarize(query: str, top_k: int = 3) -> List[dict]:
    """
    1. Embed the query
    2. Fetch top_k chunks from vector DB
    3. Summarize each chunk via Gemini LLM
    4. Return both raw text and summary
    """
    if vector_db.index.ntotal == 0:
        return []

    # 1. Embed query
    query_emb = get_embeddings([{"text": query}])[0]["embedding"]

    # 2. Retrieve top_k chunks from FAISS
    results = vector_db.query(query_emb, top_k=top_k)

    # 3. Summarize each chunk
    output = []
    for chunk in results:
        raw_text = chunk.get("text", "")
        summary = query_llm(raw_text) if raw_text else "No text available"

        output.append({
            "raw_text": raw_text,
            "summary": summary,
            "title": chunk.get("title", ""),
            "start_page": chunk.get("start_page"),
            "end_page": chunk.get("end_page")
        })

    return output
