from api.endpoints import user, login, subscriptions, request


async def setup_router(app):
    app.include_router(user.router, tags=["User"])
    app.include_router(login.router, tags=["Login"])
    app.include_router(subscriptions.router, tags=["Subscription"])
    app.include_router(request.router, tags=["Inference"])

    @app.get("/", tags=["root"])
    async def read_root() -> dict:
        return {"message": "Welcome to Housify API"}
