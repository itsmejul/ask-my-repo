import os

from dotenv import load_dotenv

load_dotenv()  # Loads from .env by default
class Config:
    DEBUG=os.getenv("DEBUG", False)
    CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_BACKEND_URL=os.getenv("CELERY_BACKEND_URL", "redis://redis:6379/0")

    QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT"))
    EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME")