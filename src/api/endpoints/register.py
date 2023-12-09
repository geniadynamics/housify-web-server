from fastapi import APIRouter, HTTPException
from tortoise.transactions import in_transaction
from src.data.models.user import User
from src.data.schemas.user import UserSchema

router = APIRouter()


@router.post("/register/", response_model=UserSchema)
async def register_user(user_data: UserSchema):
    """
    Register a new user.

    Parameters:
    - `user_data`: User data for registration.

    Returns:
    - Registered user data.
    """
    if await User.filter(email=user_data.email).exists():
        raise HTTPException(status_code=400, detail="Email already registered")


    async with in_transaction():
        created_user = await User.create(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=user_data.hashed_password,
            gender=user_data.gender,
            phone=user_data.phone,
            birth_date=user_data.birth_date,
            subscription_lvl_id=user_data.subscription_lvl_id,
        )

    return created_user
