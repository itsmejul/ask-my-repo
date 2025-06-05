
from celery import Celery
from app.config import Config

REDIS_URL = "redis://redis:6379/0"#TODO import from config
celery_worker = Celery('indexing_service',
                broker=REDIS_URL,
                backend=REDIS_URL#,
                #include=["tasks.index_repo"] # Achtung, das ist relativ zu wo celery ausgeführt wird!
                )
celery_worker.autodiscover_tasks(['app'])