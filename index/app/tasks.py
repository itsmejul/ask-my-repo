from app.utils import clone_repo, temp_repo_path, read_directory_documents, create_index
# warum app.utils statt utils?
import redis
import subprocess
from celery_worker import celery_worker

# TODO check if the same repo is already being indexed before starting the task
# TODO delete /temp/key if something goes wrong
# TODO poll this to see when it is done
@celery_worker.task(bind=True, max_retries = 3, name="index_repo")
def index_repo(self, url, url_id):
    r = redis.Redis(host="redis", port=6379, decode_responses=True)
    try:
        temp_path = temp_repo_path(url_id) # Path to clone the repo
        clone_repo(repo_url=url, target_dir=temp_path)

        documents = read_directory_documents(temp_path)
        print("Creating index...")
        create_index(documents, url_id)
        subprocess.run(["rm", "-rf", "./temp"])

        r.set(f"repo_status:{url_id}", "done")
    except Exception as e:
        r.set(f"repo_status:{url_id}", "failed")
        print("error " + str(e))
    
    return "finished"



