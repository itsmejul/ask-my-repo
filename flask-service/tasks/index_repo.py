from utils import hash_repo_url, clone_repo, temp_repo_path

from celery_worker import app

# TODO check if the same repo is already being indexed before starting the task
# TODO delete /temp/key if something goes wrong
# TODO poll this to see when it is done
@app.task(bind=True, max_retries = 3, name="index_repot")
def index_repot(self, repo_url):
    key = hash_repo_url(repo_url)
    temp_path = temp_repo_path(key) # Path to clone the repo
    try:
        clone_repo(repo_url=repo_url, target_dir=temp_path)
    except Exception(e):
        print("error " + e)
    
    return "finished"
