import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "core.housify_service:app",
        host="0.0.0.0",
        port=8081,
        # workers=12,
        reload=True,  # Set to false when using multiple workers
    )
