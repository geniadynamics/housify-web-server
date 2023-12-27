from fastapi import APIRouter, HTTPException, Depends
from async_fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer

from services.utils.hash import hash_combined_passwd
from data.models import User
from data.schemas import LoginSchema, TokenResponse

from pathlib import Path
import os

from dotenv import load_dotenv

from core.mail_service import send_email

ui_auth_rule = HTTPBearer()
router = APIRouter()

root_path = Path(__file__).parent.parent.parent.parent
env_path = root_path / "src" / ".env"
load_dotenv(env_path)

root_dir = os.getenv("ROOT")
email_template_path = (
    Path(root_dir) / "templates/email"
    if root_dir is not None
    else Path("templates/email")
)

responses = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {"example": {"detail": "Bad email or password"}}
        },
    }
}


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={401: responses[401]},
)
async def login(user: LoginSchema, Authorize: AuthJWT = Depends()):
    try:
        db_user = await User.get(email=user.email)

        if not db_user or db_user.hashed_password != hash_combined_passwd(
            user.hashed_password.decode(), db_user.id
        ):
            raise HTTPException(status_code=401, detail="Bad email or password")
    except Exception as e:
        print(e) # !TODO add log
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
        "refresh_token": await Authorize.create_refresh_token(subject=db_user.id.hex),
    }


denylist = set()


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in denylist


@router.post("/login/refresh")
async def refresh(Authorize: AuthJWT = Depends()):
    await Authorize.jwt_refresh_token_required()

    current_user = await Authorize.get_jwt_subject()
    if not current_user:
        return {"detail": "Invalid token"}, 401

    new_access_token = await Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.delete("/logout/access-revoke", dependencies=[Depends(ui_auth_rule)])
async def access_revoke(Authorize: AuthJWT = Depends()):
    await Authorize.jwt_required()
    raw_jwt = await Authorize.get_raw_jwt()
    if raw_jwt is None:
        return {"detail": "Invalid token"}, 401

    jti = raw_jwt["jti"]

    denylist.add(jti)
    return {"detail": "Access token has been revoke"}


@router.delete("/logout/refresh-revoke", dependencies=[Depends(ui_auth_rule)])
async def refresh_revoke(Authorize: AuthJWT = Depends()):
    await Authorize.jwt_refresh_token_required()

    raw_jwt = await Authorize.get_raw_jwt()
    if raw_jwt is None:
        return {"detail": "Invalid token"}, 401

    jti = raw_jwt["jti"]

    denylist.add(jti)
    return {"detail": "Refresh token has been revoke"}


@router.post("/protected", dependencies=[Depends(ui_auth_rule)])
async def protected(Authorize: AuthJWT = Depends()):
    await Authorize.jwt_required()

    print(Authorize._access_token_expires)

    current_user = await Authorize.get_jwt_subject()
    return {"user": current_user}
