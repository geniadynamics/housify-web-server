from fastapi import FastAPI, Request
from tortoise.contrib.fastapi import register_tortoise
from api.endpoints import user, login
from services.crud.subscription_lvl import create_default_subscription_lvl
from tortoise import Tortoise
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.openapi.utils import get_openapi

from fastapi.responses import JSONResponse
from core.orm_config import config_db

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from redis.asyncio import Redis
from services.auth import jwt
from pathlib import Path

import os

app = FastAPI()

app.include_router(user.router, tags=[""])
app.include_router(login.router, tags=[""])


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to Housify API"}


DATABASE_CONFIG = config_db()


root_dir = os.getenv("ROOT")
email_template_path = (
    Path(root_dir) / "templates/email"
    if root_dir is not None
    else Path("templates/email")
)


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=os.getenv("MAIL_PORT"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
    MAIL_SSL_TLS=True,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=email_template_path,
)


async def on_startup():
    await Tortoise.init(config=DATABASE_CONFIG)
    await Tortoise.generate_schemas()

    await create_default_subscription_lvl()
    await jwt.setup()


app.add_event_handler("startup", on_startup)


register_tortoise(
    app,
    config=DATABASE_CONFIG,
    generate_schemas=False,
    add_exception_handlers=True,
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Your API Title",
#         version="Your API Version",
#         description="Your API Description",
#         routes=app.routes,
#     )
#     # Define security scheme for JWT Authorization
#     openapi_schema["components"]["securitySchemes"] = {
#         "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
#     }
#     # Apply it to all the paths
#     for path in openapi_schema["paths"].values():
#         for method in path.values():
#             # Each path method gets a list of security schemes
#             method.setdefault("security", [])
#             method["security"].append({"bearerAuth": []})
#
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema
#
#
# app.openapi = custom_openapi
