import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.service.application:create_app", factory=True, port=5000, log_level="debug", reload=True, use_colors=True
    )
