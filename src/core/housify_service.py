from fastapi import FastAPI
from services.crud.subscription_lvl import create_default_subscription_lvl
from tortoise import Tortoise

from core.orm_config import config_db, register_orm

from api.router import setup_router

from services.auth import jwt
from core.redis_client import get_redis_client
from core.load_env import load_env
from core.mail_service import setup_email_connection
from services.utils.cutom_openapi import setup_openapi
  
from zeep import Client
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from fastapi import Request


app = FastAPI()


async def on_startup():
    global app

    await load_env()
    await setup_email_connection()
    await Tortoise.init(config=config_db())
    await Tortoise.generate_schemas()
    await register_orm(app)

    await get_redis_client()
    await jwt.setup()
    await create_default_subscription_lvl()
    await setup_openapi(app)
    await setup_router(app)


app.add_event_handler("startup", on_startup)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


# soap_client = Client("http://localhost:5000/CryptoRateService.svc?wsdl")
#
#
# @app.get("/soap/crypto-rate/{symbol}")
# async def get_crypto_rate(symbol: str):
#     """
#     Uses SOAP to get the cryptocurrency rate for a specified symbol
#     """
#     response = soap_client.service.GetCryptoRate(symbol)
#     return {"symbol": response.Symbol, "price": response.Price}
#
#
# @app.get("/soap/all-crypto-rates")
# async def get_all_crypto_rates():
#     """
#     Uses SOAP to get all cryptocurrency rates stored in the database.
#     """
#     responses = soap_client.service.GetAllCryptoRates()
#     return [{"symbol": rate.Symbol, "price": rate.Price} for rate in responses]
