import os
#from dotenv import load_dotenv

#load_dotenv()  # Loads from .env by default

#TODO make example .env files
class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
    N_RETRIEVAL_RESULTS = int(os.getenv("N_RETRIEVAL_RESULTS"))
    EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME")
    DEBUG = os.getenv("DEBUG", False)
    REDIS_URL = os.getenv("REDIS_URL")