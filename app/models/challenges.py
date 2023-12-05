from beanie import Document
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from pymongo import IndexModel

class ChallengeBase(BaseModel):
    title: str
    region: str
    layer: str
    description: str
    connect: str
    flag: str

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeUpdate(ChallengeBase):
    pass

class ChallengeInDB(ChallengeBase):
    id: str

class Challenge(Document, ChallengeInDB):
    class Settings:
        collection = "challenges"

        indexes = [
            IndexModel("id", unique=True),
        ]
