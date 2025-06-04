# app/routes/main.py
from flask import Blueprint, request, jsonify
import requests
from app.utils import hash_repo_url, exists_repo

QDRANT_URL = "http://qdrant:6333" #TODO make it like this using network in compose "http://qdrant:6333"
RETRIEVE_URL = "http://retrieve:5010"
api_bp = Blueprint("api", __name__)

@api_bp.route("/health")
def health():
    return {"status": "hello"}, 200


@api_bp.route("/repo/id", methods=["POST"])
def id_repo():
    data = request.get_json()
    url = data.get("url")
    url_id = hash_repo_url(url)
    return {"id": url_id}, 200

# TODO write tests for this method
# TODO check not only in database, but check if it is currently in a celery worker
@api_bp.route("/repo/check", methods=["Post"])
def check_repo():
    data = request.get_json()
    url = data.get("url")
    url_id = hash_repo_url(url)
    exists = exists_repo(url_id)
    return {"exists" : exists}, 200

@api_bp.route("/repo/query", methods=["POST"])
def query_repo():
    data = request.get_json()
    url = data.get("url")
    url_id = hash_repo_url(url)

    exists = exists_repo(url_id)
    if exists:
        res = requests.post(RETRIEVE_URL + "/health", None)
        pass
    else:
        pass 
        # Send request to index microservice, start celery, and return redis process id to frontend for polling
    return res.json()