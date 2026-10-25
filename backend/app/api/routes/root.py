
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {"message": "Ask Your Documents API is running1"}
