from data.schemas.user import UserRegisterSchema
from data.models.user import User
from services.utils.hash import hash_combined_passwd
import uuid


async def create_user(
    user_data: UserRegisterSchema,
) -> User:
    assigned_id = uuid.uuid4()
    hashed_password = hash_combined_passwd(user_data.hashed_password, assigned_id)

    user = await User.create(
        id=assigned_id,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=hashed_password,
        gender=user_data.gender,
        phone=user_data.phone,
        birth_date=user_data.birth_date,
        subscription_lvl="Free-Tier",
    )

    return user


async def get_id_with_email(email: str) -> str:
    return (await User.get(email=email)).id.hex
