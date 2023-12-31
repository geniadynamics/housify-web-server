from api.endpoints import user, login, subscriptions


async def setup_router(app):
    app.include_router(user.router, tags=[""])
    app.include_router(login.router, tags=[""])
    app.include_router(subscriptions.router, tags=[""])

    @app.get("/", tags=["root"])
    async def read_root() -> dict:
        return {"message": "Welcome to Housify API"}
