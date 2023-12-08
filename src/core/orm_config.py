from dotenv import load_dotenv
import os
from pathlib import Path

root_path = Path(__file__).parent.parent.parent


def config_db():
    """ """

    env_path = root_path / "src" / ".env"
    load_dotenv(env_path)

    ENV = os.getenv("ENV", "development")
    DB_URL = (
        os.getenv("PROD_DB_URL") if ENV == "production" else os.getenv("DEV_DB_URL")
    )
    print(DB_URL)

    return {
        "connections": {"default": DB_URL},
        "apps": {
            "models": {
                "models": [
                    "data.models.user",
                    "data.models.device_login",
                    "data.models.payment",
                    "data.models.address",
                    "data.models.device",
                    "data.models.invoice",
                    "data.models.subscription",
                    "data.models.subscription_lvl",
                    "data.models.refresh_token",
                    "data.models.credit_card",
                    "data.models.billing_info",
                ],
                "default_connection": "default",
            },
        },
    }
