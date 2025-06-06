
from celery import Celery
import os
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
REDIS_URL = "redis://" + redis_host + ":" + redis_port + "/0"
#REDIS_URL = "redis://redis:6379/0"
import sys
print("PYTHONPATH:", sys.path, flush=True)
import pkgutil
import app  # must be importable

print("Submodules in 'app':")
for module_info in pkgutil.walk_packages(app.__path__, prefix="app."):
    print(module_info.name)


from huggingface_hub import login
import os 
login(token=os.environ["HUGGINGFACE_HUB_TOKEN"])
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

embed_model_name = os.getenv("EMBED_MODEL_NAME")
Settings.embed_model = HuggingFaceEmbedding(
    model_name=embed_model_name
)

celery_worker = Celery('indexing_service',
                broker=REDIS_URL,
                backend=REDIS_URL#,
                #include=["app.app.tasks.index_repo"] # Achtung, das ist relativ zu wo celery ausgeführt wird!
                )
celery_worker.autodiscover_tasks(['app.tasks'])