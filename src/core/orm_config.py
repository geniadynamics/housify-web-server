from dotenv import load_dotenv
import os
from pathlib import Path


def config_db():
    """ """

    ENV = os.getenv("ENV", "dev")
    DB_URL = (
        os.getenv("PROD_DB_URL") if ENV == "prod" else os.getenv("DEV_DB_URL")
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
