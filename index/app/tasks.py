import os
import redis
import subprocess

from celery_worker import celery_worker
from app.utils import clone_repo, temp_repo_path, read_directory_documents, create_index

# TODO check if the same repo is already being indexed before starting the task
# TODO delete /temp/key if something goes wrong
@celery_worker.task(bind=True, max_retries = 3, name="index_repo")
def index_repo(self, url, url_id):
    '''
    Celery task for indexing a github repo via its url and save it in a qdrant collection corresponding to the url_id
    '''
    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT")
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    temp_path = temp_repo_path(url_id)
    try:
        clone_repo(repo_url=url, target_dir=temp_path)

        documents = read_directory_documents(temp_path)
        print("Creating index...")
        create_index(documents, url_id)
        subprocess.run(["rm", "-rf", temp_path]) #TODO check this works with temp path instead of "./temp" ?

        r.set(f"repo_status:{url_id}", "done")
    except Exception as e:
        r.set(f"repo_status:{url_id}", "failed")
        subprocess.run(["rm", "-rf", temp_path]) #TODO check this works with temp path instead of "./temp" ?
        print("error " + str(e))
    
    return "finished"



