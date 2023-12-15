from data.schemas.user import UserRegisterSchema, UserSchema
from fastapi import APIRouter, HTTPException, status
from services.crud.user import create_user
from data.models.user import User
import uuid

router = APIRouter()


@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_user(user_data: UserRegisterSchema):
    user = await create_user(user_data)
    if not user:
        raise HTTPException(status_code=400, detail="Error creating user")
    return user


# ADD auth requirements
@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: uuid.UUID):
    user = await User.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
