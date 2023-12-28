from fastapi import APIRouter, HTTPException, Depends
from async_fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer

from services.utils.hash import hash_combined_passwd
from data.models import User
from data.schemas import LoginSchema, TokenResponse

from core.mail_service import send_email
from api.reponses import responses
from core.redis_client import get_redis_client

from services.auth.jwt import validate_access_token, validate_refresh_token

ui_auth_rule = HTTPBearer()
router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={401: responses[401]},
)
async def login(user: LoginSchema, Authorize: AuthJWT = Depends()):
    """
    Authenticate a user and provide access and refresh tokens.

    This endpoint authenticates a user based on their email and password.
    If authentication is successful, it sends an email notification and
    returns an access token and a refresh token.

    Args:
        user (LoginSchema): A pydantic schema representing the user's login details.
        Authorize (AuthJWT, optional): Dependency injection for JWT authorization.
                                       Defaults to Depends().

    Returns:
        dict: A dictionary containing the 'access_token' and 'refresh_token'.

    Raises:
        HTTPException: If authentication fails with a 401 status code,
                       indicating a bad email or password.
    """

    try:
        db_user = await User.get(email=user.email)

        if not db_user or db_user.hashed_password != hash_combined_passwd(
            user.hashed_password.decode(), db_user.id
        ):
            raise HTTPException(status_code=401, detail="Bad email or password")
        subject = "Login Sucessful Housify"
        recipients = [user.email]
        body_content = {
            "title": "Login Successful",
            "name": f"{db_user.first_name} {db_user.last_name}",
        }

        await send_email(subject, recipients, body_content)

        return {
            "access_token": await Authorize.create_access_token(subject=db_user.id.hex),
            "refresh_token": await Authorize.create_refresh_token(
                subject=db_user.id.hex
            ),
        }
    except Exception as e:
        print(e)  # !TODO add log
        raise HTTPException(status_code=401, detail="Bad email or password")


@router.post("/login/refresh", dependencies=[Depends(ui_auth_rule)])
async def refresh(
    Authorize: AuthJWT = Depends(), redis_client=Depends(get_redis_client)
):
    """
    Refresh the access token using a valid refresh token.

    This endpoint creates a new access token for a user with a valid refresh token.

    Args:
        Authorize (AuthJWT): Dependency injection for JWT authorization.
        redis_client (callable, optional): Dependency for Redis client.
                                           Defaults to Depends(get_redis_client).

    Returns:
        dict: A dictionary containing the new 'access_token'.

    Raises:
        HTTPException: If the refresh token is invalid, with a 401 status code.
    """

    await validate_refresh_token(Authorize, redis_client)

    current_user = await Authorize.get_jwt_subject()
    if not current_user:
        return {"detail": "Invalid token"}, 401

    new_access_token = await Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.delete("/logout/access-revoke", dependencies=[Depends(ui_auth_rule)])
async def access_revoke(
    Authorize: AuthJWT = Depends(), redis_client=Depends(get_redis_client)
):
    await Authorize.jwt_required()
    raw_jwt = await Authorize.get_raw_jwt()
    if raw_jwt is None:
        return {"detail": "Invalid token"}, 401

    jti = raw_jwt["jti"]
    redis_client.sadd("denylist", jti)
    return {"detail": "Access token has been revoke"}


@router.delete("/logout/refresh-revoke", dependencies=[Depends(ui_auth_rule)])
async def refresh_revoke(
    Authorize: AuthJWT = Depends(), redis_client=Depends(get_redis_client)
):
    await Authorize.jwt_refresh_token_required()

    raw_jwt = await Authorize.get_raw_jwt()
    if raw_jwt is None:
        return {"detail": "Invalid token"}, 401

    jti = raw_jwt["jti"]
    redis_client.sadd("denylist", jti)
    return {"detail": "Refresh token has been revoke"}


@router.post("/protected", dependencies=[Depends(ui_auth_rule)])
async def protected(
    Authorize: AuthJWT = Depends(), redis_client=Depends(get_redis_client)
):
    await validate_access_token(Authorize, redis_client)

    current_user = await Authorize.get_jwt_subject()
    return {"user": current_user}
