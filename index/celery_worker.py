from celery import Celery
import os
from huggingface_hub import login
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_url = "redis://" + redis_host + ":" + redis_port + "/0"
import app
login(token=os.environ["HUGGINGFACE_HUB_TOKEN"])
embed_model_name = os.getenv("EMBED_MODEL_NAME")

Settings.embed_model = HuggingFaceEmbedding(
    model_name=embed_model_name
)

celery_worker = Celery('indexing_service',
                broker=redis_url,
                backend=redis_url#,
                #include=["app.app.tasks.index_repo"] # Achtung, das ist relativ zu wo celery ausgeführt wird!
                )
celery_worker.autodiscover_tasks(['app.tasks']) # Note that we need to import app first, otherwise it will not find it