import logging
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.router import task_routes, user_routes

logger = logging.getLogger(__name__)

app = FastAPI(
  title="To-Do API",
  version="0.1.0",
  docs_url="/docs",
  redoc_url="/redoc"
)

app.add_middleware(
  CORSMiddleware,
  allow_origins = settings.BACKEND_CORS_ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(task_routes.router)
app.include_router(user_routes.router)

@app.get("/")
def read_root():
  return {"message": "Hello World"}

@app.get("/health", tags=["Health"])
async def health():
  return {"status": "ok"}
