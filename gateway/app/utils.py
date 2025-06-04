from urllib.parse import urlparse
import hashlib
import requests
#from git import Repo 
from pathlib import Path

QDRANT_URL = "http://qdrant:6333" #TODO make it like this using network in compose "http://qdrant:6333"

def sanitize_repo_url(url: str) -> str:
    """
    Extracts 'owner/repo' from a GitHub URL like:
    https://github.com/owner/repo/blob/branch/path/to/file
    """
    parsed = urlparse(url)
    parts = parsed.path.strip('/').split('/')
    if len(parts) < 2:
        raise ValueError("URL must include at least 'owner/repo'")
    owner, repo = parts[0], parts[1]
    return f"{owner}/{repo}"

def hash_repo_url(url: str) -> str:
    sanitized_url = sanitize_repo_url(url)
    return hashlib.sha1(sanitized_url.encode()).hexdigest()[:32]

# TODO add try catch for api request to qdrants
def exists_repo(id):
    res = requests.get(QDRANT_URL + "/collections", json = None)
    collections = res.json().get("result").get("collections")
    collections = [collection.get("name") for collection in collections]
    print(collections)
    if id in collections:
        return True 
    else:
        return False