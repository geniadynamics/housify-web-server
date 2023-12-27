from fastapi.openapi.utils import get_openapi


async def setup_openapi(app):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Your API Title",
            version="Your API Version",
            description="Your API Description",
            routes=app.routes,
        )
        # Define security scheme for JWT Authorization
        # openapi_schema["components"]["securitySchemes"] = {
        #     "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        # }
        # Apply it to all the paths
        # for path in openapi_schema["paths"].values():
        #     for method in path.values():
        #         # Each path method gets a list of security schemes
        #         method.setdefault("security", [])
        #         method["security"].append({"bearerAuth": []})

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
