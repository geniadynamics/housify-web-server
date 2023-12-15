from data.models.subscription_lvl import SubscriptionLvl


async def create_default_subscription_lvl():
    default_levels = {
        "Free-Tier": {
            "price": 0.00,
            "upload_size_limit": 100,  # MB
            "storage_limit": 10,  # GB
            "its": 2.5,
            "api_key_limit": 1,
            "requests_hour": 6,
            "watermark": True,
        },
        "Pro-Tier": {
            "price": 9.99,
            "upload_size_limit": 1000,  # MB
            "storage_limit": 100,  # GB
            "its": 5.0,
            "api_key_limit": 10,
            "requests_hour": 60,
            "watermark": False,
        },
    }

    for description, attributes in default_levels.items():
        if not await SubscriptionLvl.filter(description=description).exists():
            subscription_lvl = SubscriptionLvl(description=description, **attributes)
            await subscription_lvl.save()
            print(f"Default {description} subscription level created")
        else:
            print(f"Default {description} subscription level already exists")
