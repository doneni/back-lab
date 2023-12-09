from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.challenges import Challenge
from app.schemas.challenges import ChallengeBase
from app.models.users import User
from app.auth.auth import get_current_user

router = APIRouter()

@router.get("/")
async def root_challenge():
    return {"message": "Welcome to challenge home !"}


@router.get("/get-all-challenges", response_model=dict)
async def get_all_challenges():
    challenges = await Challenge.all().to_list()
    challenges_base = [ChallengeBase(
        title=challenge.title,
        region=challenge.region,
        layer=challenge.layer,
        description=challenge.description,
        connect=challenge.connect
    ) for challenge in challenges]
    return {"challenges": challenges_base}


# @router.get("/get-challenges", response_model=ChallengeBase)
# async def get_challenges(current_user: User = Depends(get_current_user)):
#     challenges = await Challenge.all().to_list()
#     solved_challenge_uuids = set(current_user.solved)
#     challenges_with_solved_status = [
#         {
#             "uuid": str(challenge.uuid),
#             "title": challenge.title,
#             "flag": challenge.flag,
#             "solved": str(challenge.uuid) in solved_challenge_uuids,
#         }
#         for challenge in challenges
#     ]
#     return challenges_with_solved_status


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