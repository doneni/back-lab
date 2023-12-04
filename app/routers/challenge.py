from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_challenge():
    return {"message": "Get Challenge Home !"}