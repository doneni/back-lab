from fastapi import APIRouter, HTTPException
from typing import List

from ..models.challenges import Challenge
from ..schemas.challenges import ChallengeCreate

router = APIRouter()

# @router.get("/")
# async def root():
#     return {"message": "Get Challenge Home !"}

@router.get("/", response_model=List[Challenge])
async def get_challenges():
    try:
        challenges = await Challenge.all()
        return challenges
    except Exception as e:
        return {"error": f"An error occurred: {e}"}