import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.endpoints import task_ep, user_ep

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

app.include_router(task_ep.router)
app.include_router(user_ep.router)

@app.get("/")
def read_root():
  """Return a greeting payload for health checks.

  Returns:
    dict[str, str]: Static message confirming the API is reachable.
  """
  return {"message": "Hello World"}

@app.get("/health", tags=["Health"])
async def health():
  """Expose a liveness endpoint for monitoring tools.

  Returns:
    dict[str, str]: Status payload indicating the service is operational.
  """
  return {"status": "ok"}
