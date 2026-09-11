
from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.projects import router as projects_router
from app.routers.endpoints import router as endpoints_router
from app.routers.analysis import router as analysis_router
from app.routers.summary import router as summary_router
from app.routers.admin import router as admin_router
from app.config import ALLOWED_ORIGINS


Base.metadata.create_all(
    bind=engine,
)


app = FastAPI(
    title="AI API Documentation & Testing Assistant",
    description=(
        "Backend service for AI-powered API documentation, "
        "testing, and security analysis."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(endpoints_router)
app.include_router(analysis_router)
app.include_router(summary_router)
app.include_router(admin_router)

@app.get(
    "/",
    tags=["System"],
)
def root():
    return {
        "name": "AI API Documentation & Testing Assistant",
        "status": "running",
    }


@app.get(
    "/health",
    tags=["System"],
)
def health():
    return {
        "status": "healthy",
    }

