
from fastapi import APIRouter, Depends, HTTPException
from app.models.challenges import Challenge
from app.schemas.challenges import ChallengeBase
from app.models.users import User
from app.auth.auth import get_current_user

router = APIRouter()

@router.get("/")
async def root_challenge():
    return {"message": "Welcome to challenge home !"}

@router.get("/get-challenges", response_model=ChallengeBase)
async def get_all_challenges():
    challenges = await Challenge.all().to_list()
    return {"challenges": challenges}

@router.post("/check-flag")
async def check_flag(
        title: str,
        user_flag: str,
        current_user: User = Depends(get_current_user),
):
    challenge = await Challenge.find_one({"title": title, "flag": user_flag})
    if challenge:
        current_user.solved.append(str(challenge.uuid))
        await current_user.save()
        return {"message": "correct flag"}
    else:
        return {"message": "incorrect flag"}