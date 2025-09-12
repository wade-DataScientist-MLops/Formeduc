from fastapi import APIRouter
from core.solenys_logic import ask_solenys

router = APIRouter()

@router.get("/solenys_query")
async def solenys_query(q: str):
    response = ask_solenys(q)
    return {"answer": response["text"]}
