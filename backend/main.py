from fastapi import FastAPI
from app.core.database import init_db

app = FastAPI(title="São Paulo Gas Price Tracker API")


@app.on_event("startup")
def startup_event():
    """Initialize database on application startup."""
    init_db()


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
