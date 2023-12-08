from fastapi import FastAPI, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise

from data.schemas.subscription_lvl import SubscriptionLvlSchema
from data.models.subscription_lvl import SubscriptionLvl

from core.orm_config import config_db

DATABASE_CONFIG = config_db()

app = FastAPI()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!"}


@app.post(
    "/api/subscription_lvl",
    response_model=SubscriptionLvlSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription_lvl(subscription_data: SubscriptionLvlSchema):
    """
    POST - Create Housify subscription level
    """
    subscription_lvl = SubscriptionLvl(**subscription_data.model_dump())
    subscription_lvl.is_active = True
    await subscription_lvl.save()
    return subscription_lvl


register_tortoise(
    app,
    config=DATABASE_CONFIG,
    generate_schemas=True,
    add_exception_handlers=True,
)
