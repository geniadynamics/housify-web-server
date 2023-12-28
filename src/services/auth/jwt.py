from async_fastapi_jwt_auth import AuthJWT
from datetime import timedelta
import os

from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import HTTPException

ALGORITHM = "ES512"

key_path = os.getenv("ECDSA_KEY_PATH")


async def setup():
    def load_ecdsa_key(file_path: str):
        with open(file_path, mode="r") as file:
            return file.read()

    def load():
        return (
            load_ecdsa_key(key_path if key_path else "" + "ec_private.pem"),
            load_ecdsa_key(key_path if key_path else "" + "ec_public.pem"),
        )

    private_key, public_key = load()

    config = {
        "authjwt_algorithm": "ES512",
        "authjwt_public_key": public_key,
        "authjwt_private_key": private_key,
        "authjwt_access_token_expires": timedelta(minutes=5),
        "authjwt_refresh_token_expires": timedelta(days=7),
    }

    @AuthJWT.load_config
    def get_config():
        return [(key, value) for key, value in config.items()]


async def is_token_in_denylist(jti, redis_client):
    """Check if the token's JTI is in the Redis denylist."""
    return redis_client.sismember("denylist", jti)


async def validate_access_token(Authorize, redis_client):
    """An exeption is trown when the token is invalid or in deny list"""
    await Authorize.jwt_required()

    raw_jwt = await Authorize.get_raw_jwt()
    if raw_jwt is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    jti = raw_jwt["jti"]
    if await is_token_in_denylist(jti, redis_client):
        raise HTTPException(status_code=401, detail="Token has been revoked")


async def validate_refresh_token(Authorize, redis_client):
    """An exeption is trown when the token is invalid or in deny list"""
    await Authorize.jwt_required()

    raw_jwt = await Authorize.get_raw_jwt()
    if raw_jwt is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    jti = raw_jwt["jti"]
    if await is_token_in_denylist(jti, redis_client):
        raise HTTPException(status_code=401, detail="Token has been revoked")
