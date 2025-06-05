from celery import Celery



REDIS_URL = "redis://localhost:6379/0"
app = Celery('tasks',
                broker=REDIS_URL,
                backend=REDIS_URL,
                include=["tasks.index_repo"] # Achtung, das ist relativ zu wo celery ausgeführt wird!
                )
#app.autodiscover_tasks(['tasks'])