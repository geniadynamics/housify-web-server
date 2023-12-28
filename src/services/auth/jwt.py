from async_fastapi_jwt_auth import AuthJWT
from datetime import timedelta
import os
from fastapi import HTTPException

ALGORITHM = "ES512"
key_path = os.getenv("ECDSA_KEY_PATH")


async def setup():
    """
    Set up JWT authentication by loading ECDSA keys and configuring AuthJWT.

    This function loads the ECDSA private and public keys from files and sets
    up the JWT authentication configuration for AuthJWT.

    Raises:
        FileNotFoundError: If the key files are not found.
    """

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
        "authjwt_algorithm": ALGORITHM,
        "authjwt_public_key": public_key,
        "authjwt_private_key": private_key,
        "authjwt_access_token_expires": timedelta(minutes=5),
        "authjwt_refresh_token_expires": timedelta(days=7),
    }

    @AuthJWT.load_config
    def get_config():
        return [(key, value) for key, value in config.items()]


async def is_token_in_denylist(jti, redis_client):
    """
    Check if a token's JTI (JSON Token Identifier) is in the denylist.

    Args:
        jti (str): The JTI of the token.
        redis_client: The Redis client for interacting with the denylist.

    Returns:
        bool: True if the token's JTI is in the denylist, False otherwise.
    """
    return redis_client.sismember("denylist", jti)


async def validate_access_token(Authorize, redis_client):
    """
    Validate an access token and check if it's in the denylist.

    Args:
        Authorize (AuthJWT): The AuthJWT instance for token validation.
        redis_client: The Redis client for interacting with the denylist.

    Raises:
        HTTPException: If the token is invalid or revoked, with a 401 status code.
    """
    await Authorize.jwt_required()

    raw_jwt = await Authorize.get_raw_jwt()
    if raw_jwt is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    jti = raw_jwt["jti"]
    if await is_token_in_denylist(jti, redis_client):
        raise HTTPException(status_code=401, detail="Token has been revoked")


async def validate_refresh_token(Authorize, redis_client):
    """
    Validate a refresh token and check if it's in the denylist.

    Args:
        Authorize (AuthJWT): The AuthJWT instance for token validation.
        redis_client: The Redis client for interacting with the denylist.

    Raises:
        HTTPException: If the token is invalid or revoked, with a 401 status code.
    """
    await Authorize.jwt_refresh_token_required()

    raw_jwt = await Authorize.get_raw_jwt()
    if raw_jwt is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    jti = raw_jwt["jti"]
    if await is_token_in_denylist(jti, redis_client):
        raise HTTPException(status_code=401, detail="Token has been revoked")
