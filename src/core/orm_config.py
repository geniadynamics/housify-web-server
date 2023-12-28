import os
from tortoise.contrib.fastapi import register_tortoise


def config_db():
    """ """

    ENV = os.getenv("ENV", "development")
    DB_URL = (
        os.getenv("PROD_DB_URL") if ENV == "production" else os.getenv("DEV_DB_URL")
    )

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
                    "data.models.credit_card",
                    "data.models.billing_info",
                ],
                "default_connection": "default",
            },
        },
    }


async def register_orm(app):
    register_tortoise(
        app,
        config=config_db(),
        generate_schemas=False,
        add_exception_handlers=True,
    )
