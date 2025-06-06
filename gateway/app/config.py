import os

class Config:
    QDRANT_HOST = os.getenv("QDRANT_HOST")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT"))

    FRONTEND_HOST = os.getenv("FRONTEND_HOST")
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT"))