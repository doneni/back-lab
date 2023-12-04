from fastapi import APIRouter

from . import login, users, challenge, story

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(challenge.router, prefix="/challenge", tags=["challenge"])
api_router.include_router(story.router, prefix="/story", tags=["story"])

@api_router.get("/")
async def root():
    return {"message": "Backend API for FARM-docker operational !"}
