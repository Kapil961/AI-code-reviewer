from fastapi import FastAPI
from app.routers import review


app = FastAPI(
    title="AI Code Reviewer",
    description="AI powered repository code review system",
    version="1.0"
)


app.include_router(
    review.router
)


@app.get("/")
def root():

    return {
        "message": "AI Code Reviewer API running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }