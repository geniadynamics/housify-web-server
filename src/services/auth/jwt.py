from async_fastapi_jwt_auth import AuthJWT
from datetime import timedelta
import os

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
        "authjwt_denylist_token_checks": {"access", "refresh"},
        "access_expires": timedelta(minutes=1),
        "refresh_expires": timedelta(days=7),
    }

    required_keys = ["authjwt_algorithm", "authjwt_public_key", "authjwt_private_key"]

    @AuthJWT.load_config
    def get_config():
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(f"Missing configuration keys: {missing_keys}")
        return [(key, value) for key, value in config.items()]
