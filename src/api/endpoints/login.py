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

    This endpoint is designed for user authentication. It accepts user login credentials, 
    verifies them, and, upon successful authentication, issues JWT (JSON Web Token) 
    access and refresh tokens. An email notification is sent to the user as a part of this process.

    Parameters:
    - user (LoginSchema): A pydantic schema object that contains the user's email and password.

    Returns:
    - dict: A dictionary containing 'access_token' and 'refresh_token'. The 'access_token' is used 
      for user session authentication, while the 'refresh_token' is used to generate new access tokens.

    Exceptions:
    - HTTPException: Raises a 401 status code exception if authentication fails. This could be due to 
      incorrect email or password.

    Note:
    - The AuthJWT dependency is used for creating and managing JWT tokens.
    - Ensure that the credentials provided in the LoginSchema are validated before processing.
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

    Returns:
        dict: A dictionary containing the new 'access_token'.

    Raises:
        HTTPException: If the refresh token is invalid, with a 401 status code.
    """

    await validate_refresh_token(
        Authorize, redis_client, validate_sub_with_internal_id=False
    )

    current_user = await Authorize.get_jwt_subject()
    if not current_user:
        return {"detail": "Invalid token"}, 401

    new_access_token = await Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.delete("/logout/access-revoke", dependencies=[Depends(ui_auth_rule)])
async def access_revoke(
    Authorize: AuthJWT = Depends(), redis_client=Depends(get_redis_client)
):
    """
    Revoke an access token.

    This endpoint revokes the current user's access token, adding it to a denylist in Redis.

    Returns:
        dict: A dictionary with a message indicating that the access token has been revoked.

    Raises:
        HTTPException: If the access token is invalid, with a 401 status code.
    """

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
    """
    Revoke a refresh token.

    This endpoint revokes the current user's refresh token, adding it to a denylist in Redis.

    Returns:
        dict: A dictionary with a message indicating that the refresh token has been revoked.

    Raises:
        HTTPException: If the refresh token is invalid, with a 401 status code.
    """
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
    """
    Access a protected resource.

    This endpoint returns data about the current user if they have a valid access token.

    Returns:
        dict: A dictionary containing the current user's information.

    Raises:
        HTTPException: If the access token is invalid, with a 401 status code.
    """

    await validate_access_token(
        Authorize, redis_client, validate_sub_with_internal_id=False
    )

    current_user = await Authorize.get_jwt_subject()
    return {"user": current_user}
