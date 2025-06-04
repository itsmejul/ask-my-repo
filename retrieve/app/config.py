# app/config.py
import os

class Config:
    DEBUG = os.getenv("DEBUG", False)
    REDIS_URL = os.getenv("REDIS_URL")