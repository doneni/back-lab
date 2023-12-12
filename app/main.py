from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from .auth.auth import get_hashed_password
from .config.config import settings
from .models.users import User
from .models.challenges import Challenge
from .models.endings import Ending
from .routers.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup mongoDB
    app.client = AsyncIOMotorClient(
        settings.MONGO_HOST,
        settings.MONGO_PORT,
        username=settings.MONGO_USER,
        password=settings.MONGO_PASSWORD,
    )
    await init_beanie(database=app.client[settings.MONGO_DB], document_models=[User, Challenge, Ending])

    user = await User.find_one({"email": settings.FIRST_SUPERUSER})
    if not user:
        user = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_hashed_password(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
        )
        await user.create()

    # create dummy challenges
    challenge = await Challenge.find_one({"title": "TITLE1"})
    if not challenge:
        challenge = Challenge(
            title="TITLE1",
            region="REGION1",
            layer="LAYER1",
            description="DESCRIPTION1",
            connect="CONNECT1",
            flag="FLAG1",
        )
        await challenge.create()

    challenge = await Challenge.find_one({"title": "TITLE2"})
    if not challenge:
        challenge = Challenge(
            title="TITLE2",
            region="REGION2",
            layer="LAYER2",
            description="DESCRIPTION2",
            connect="CONNECT2",
            flag="FLAG2",
        )
        await challenge.create()

    challenge = await Challenge.find_one({"title": "TITLE3"})
    if not challenge:
        challenge = Challenge(
            title="TITLE3",
            region="REGION3",
            layer="LAYER3",
            description="DESCRIPTION3",
            connect="CONNECT3",
            flag="FLAG3",
        )
        await challenge.create()

    challenge = await Challenge.find_one({"title": "TITLE4"})
    if not challenge:
        challenge = Challenge(
            title="TITLE4",
            region="REGION4",
            layer="LAYER4",
            description="DESCRIPTION4",
            connect="CONNECT4",
            flag="FLAG4",
        )
        await challenge.create()

    ending = await Ending.find_one({"index": 0})
    if not ending:
        ending = Ending(
            index=0,
            title="TITLE0",
            description="DESCRIPTION0",
            image="IMAGE0",
            condition=["TITLE0"]
        )
        await ending.create()

    ending = await Ending.find_one({"index": 1})
    if not ending:
        ending = Ending(
            index=1,
            title="TITLE1",
            description="DESCRIPTION1",
            image="IMAGE1",
            condition=["TITLE1"]
        )
        await ending.create()

    ending = await Ending.find_one({"index": 12})
    if not ending:
        ending = Ending(
            index=12,
            title="TITLE12",
            description="DESCRIPTION12",
            image="IMAGE12",
            condition=["TITLE1", "TITLE2"]
        )
        await ending.create()

    # yield app
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            # See https://github.com/pydantic/pydantic/issues/7186 for reason of using rstrip
            str(origin).rstrip("/")
            for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
