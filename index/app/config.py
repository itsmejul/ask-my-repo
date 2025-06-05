import os

from dotenv import load_dotenv

load_dotenv()  # Loads from .env by default
class Config:
    DEBUG=os.getenv("DEBUG", False)
    CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_BACKEND_URL=os.getenv("CELERY_BACKEND_URL", "redis://redis:6379/0")