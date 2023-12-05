from typing import Optional
from uuid import UUID, uuid4
from itertools import count

from beanie import Document
from pydantic import Field
from pymongo import IndexModel

def sequential_uuid():
    for i in count(start=1):
        yield UUID(int=i)

class Challenge(Document):
    uuid: UUID = Field(default_factory=sequential_uuid, alias="_id")
    title: str = Field(default="TITLE")
    region: str = Field(default="REGION")
    layer: str = Field(default="LAYER")
    description: str = Field(default="DESCRIPTION")
    connect: Optional[str] = Field(default="CONNECT")
    flag: str = Field(default="FLAG")

    class Settings:
        indexes = [
            IndexModel("uuid", unique=True),
        ]
