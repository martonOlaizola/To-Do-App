from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
  DATABASE_URL: str
  BACKEND_CORS_ORIGINS: List[str] = []
  SECRET_KEY: str
  ALGORITHM: str

  @field_validator("BACKEND_CORS_ORIGINS", mode="before")
  def assemble_cors(cls, v):
    if isinstance(v, str):
        return [i.strip() for i in v.split(",") if i.strip()]
    return v
  
  class Config:
    env_file =".env"

settings = Settings()