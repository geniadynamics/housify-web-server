from fastapi import APIRouter, Depends, HTTPException, status, Depends
from data.schemas import SubscriptionLvlSchema
from data.models.subscription_lvl import SubscriptionLvl
from data.schemas.login import EmailIn
from services.auth.jwt import validate_access_token

router = APIRouter()


@router.get("/subscriptions", response_model=list[SubscriptionLvlSchema])
async def get_subscription_levels():
    return await SubscriptionLvl.all()


@router.get("/user/subscribe", response_model=list[SubscriptionLvlSchema])
async def subscribe(subscription_description: str, user_data: EmailIn):
    # await validate_access_token()
    # !TODO
    return await SubscriptionLvl.all()
