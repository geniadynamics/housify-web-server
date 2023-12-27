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

from zeep import Client

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

soap_client = Client("http://localhost:5000/CryptoRateService.svc?wsdl")


@app.get("/soap/crypto-rate/{symbol}")
async def get_crypto_rate(symbol: str):
    """
    Uses SOAP to get the cryptocurrency rate for a specified symbol
    """
    response = soap_client.service.GetCryptoRate(symbol)
    return {"symbol": response.Symbol, "price": response.Price}


@app.get("/soap/all-crypto-rates")
async def get_all_crypto_rates():
    """
    Uses SOAP to get all cryptocurrency rates stored in the database.
    """
    responses = soap_client.service.GetAllCryptoRates()
    return [{"symbol": rate.Symbol, "price": rate.Price} for rate in responses]


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
