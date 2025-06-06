import os

class Config:
    QDRANT_HOST = os.getenv("QDRANT_HOST")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT"))

    FRONTEND_HOST = os.getenv("FRONTEND_HOST")
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT"))

    INDEX_HOST = os.getenv("INDEX_HOST")
    INDEX_PORT = int(os.getenv("INDEX_PORT"))

    RETRIEVE_HOST = os.getenv("RETRIEVE_HOST")
    RETRIEVE_PORT = int(os.getenv("RETRIEVE_PORT"))