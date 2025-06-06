from urllib.parse import urlparse
import hashlib
import requests
from pathlib import Path
from flask import current_app

def sanitize_repo_url(url: str) -> str:
    '''
    Extracts 'owner/repo' from a GitHub URL like:
    https://github.com/owner/repo/blob/branch/path/to/file
    '''
    parsed = urlparse(url)
    parts = parsed.path.strip('/').split('/')
    if len(parts) < 2:
        raise ValueError("URL must include at least 'owner/repo'")
    owner, repo = parts[0], parts[1]
    return f"{owner}/{repo}"

def hash_repo_url(url: str) -> str:
    '''
    Sanitizes a github repo url and returns a hash id for that repo.
    '''
    sanitized_url = sanitize_repo_url(url)
    return hashlib.sha1(sanitized_url.encode()).hexdigest()[:32]

# TODO add try catch for api request to qdrants
def exists_repo(id):
    '''
    Check whether a given repository was already indexed in Qdrant.
    '''
    qdrant_host = current_app.config["QDRANT_HOST"]
    qdrant_port = current_app.config["QDRANT_PORT"]
    qdrant_url = "http://" + qdrant_host + ":" + str(qdrant_port)
    res = requests.get(qdrant_url + "/collections", json = None)
    collections = res.json().get("result").get("collections")
    collections = [collection.get("name") for collection in collections]
    if id in collections:
        return True 
    else:
        return False