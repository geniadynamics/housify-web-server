from data.schemas.user import UserRegisterSchema, UserSchema
from data.schemas.login import LoginSchemaWithToken
from data.models.user import User
from fastapi.security import HTTPBearer
from fastapi import APIRouter, Depends, HTTPException, status, Depends
from services.crud.user import create_user
from data.models.user import User
from async_fastapi_jwt_auth import AuthJWT

router = APIRouter()
ui_auth_rule = HTTPBearer()


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


@router.post(
    "/user/me", response_model=UserSchema, dependencies=[Depends(ui_auth_rule)]
)
async def get_user(data: LoginSchemaWithToken, Authorize: AuthJWT = Depends()):
    await Authorize.jwt_required()

    user = await User.get(email=data.email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
