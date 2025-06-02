"""Application entry point script."""

import uvicorn


def main() -> None:
    """Run the FastAPI application using uvicorn server."""
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)


if __name__ == "__main__":
    main()
