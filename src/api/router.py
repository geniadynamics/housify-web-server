from fastapi import Request
from api.endpoints import user, login
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse


async def setup_router(app):
    app.include_router(user.router, tags=[""])
    app.include_router(login.router, tags=[""])

    @app.get("/", tags=["root"])
    async def read_root() -> dict:
        return {"message": "Welcome to Housify API"}

