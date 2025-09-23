from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_books():
    return ["NCERT Biology", "NEET Notes"]
