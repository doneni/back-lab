# routers/challenges.py

from fastapi import APIRouter
from app.models.challenges import Challenge
from app.schemas.challenges import ChallengeBase

router = APIRouter()

@router.get("/")
async def root_challenge():
    return {"message": "Welcome to challenge home !"}

@router.get("/get-challenges", response_model=ChallengeBase)
async def get_all_challenges():
    challenges = await Challenge.all().to_list()
    return {"challenges": challenges}

@router.post("/check-flag")
async def check_flag(title: str, user_flag: str):
    challenge = await Challenge.find_one({"title": title, "flag": user_flag})
    if challenge:
        return {"message": "correct flag"}
    else:
        return {"message": "incorrect flag"}