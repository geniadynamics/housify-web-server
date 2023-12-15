from data.schemas.user import UserRegisterSchema
from data.models.user import User
from data.models.subscription_lvl import SubscriptionLvl
from services.utils.hash import hash_combined_passwd
import uuid
from tortoise.exceptions import DoesNotExist
import logging


async def create_user(user_data: UserRegisterSchema) -> User:
    assigned_id = uuid.uuid4()
    hashed_password = hash_combined_passwd(
        user_data.hashed_password.decode("utf-8"), assigned_id
    )

    subscription_lvl_instance = await SubscriptionLvl.get(
        id=user_data.subscription_lvl, is_active=True
    )
    if subscription_lvl_instance == None:
        subscription_lvl_instance = await SubscriptionLvl.get(
            description="Free-Tier", is_active=True
        )
    if subscription_lvl_instance == None:
        raise DoesNotExist

    user = await User.create(
        id=assigned_id,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=hashed_password,
        gender=user_data.gender,
        phone=user_data.phone,
        birth_date=user_data.birth_date,
        subscription_lvl=subscription_lvl_instance,
    )
    return user
