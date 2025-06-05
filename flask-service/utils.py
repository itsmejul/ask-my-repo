from urllib.parse import urlparse
import hashlib
from git import Repo 
from pathlib import Path

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

def clone_repo(repo_url: str, target_dir: str):
    from git import Repo
    Repo.clone_from(repo_url, target_dir)

def temp_repo_path(repo_key: str) -> str:
    return Path(__file__).resolve().parent / "temp" / repo_key
