from fastapi import APIRouter, Body

router = APIRouter()

@router.post("/")
def ask_question(query: dict = Body(...)):
    question = query.get('question', '')
    return {"answer": f"LLM summary for: {question}"}
