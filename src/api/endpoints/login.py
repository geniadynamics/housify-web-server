from fastapi import APIRouter, HTTPException, Depends, Header, Query
from async_fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer

from services.utils.hash import hash_combined_passwd
from data.models import User
from data.schemas import LoginSchema, TokenResponse

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
import os

from dotenv import load_dotenv

from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List, Any, Dict

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


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "default_username"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "default_password"),
    MAIL_FROM=os.getenv("MAIL_FROM", "default_email@example.com"),
    MAIL_PORT=int(
        os.getenv("MAIL_PORT", "587")
    ),  # Convert to integer and provide a default
    MAIL_SERVER=os.getenv("MAIL_SERVER", "default_smtp_server.com"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME", "Default Name"),
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=email_template_path,
)


async def send_email(subject: str, email: List[EmailStr], body: Dict[str, Any]):
    message = MessageSchema(
        subject=subject,
        recipients=email,
        template_body=body,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email.html")


@router.post("/login", response_model=TokenResponse)
async def login(user: LoginSchema, Authorize: AuthJWT = Depends()):
    db_user = await User.get(email=user.email)

    if not db_user or db_user.hashed_password != hash_combined_passwd(
        user.hashed_password.decode(), db_user.id
    ):
        raise HTTPException(status_code=401, detail="Bad email or password")

    subject = "Login Sucessful Housify"
    recipients = [user.email]  # The recipients list should contain email strings
    body_content = {
        "title": "Login Successful",  # This will be used in <h1>{{ body.title }}</h1>
        "name": f"{db_user.first_name} {db_user.last_name}",  # This will be used in <h3>{{ body.name }}!</h3>
    }

    # Call send_email with the defined content
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