from flask import Blueprint, request, jsonify, current_app
import requests
from celery_worker import celery_worker
from app.tasks import index_repo

api_bp = Blueprint("api", __name__)

@api_bp.route("/index", methods=["POST"])
def index_start():
    data = request.get_json()
    url = data.get("url")
    url_id = data.get("id")
    
    #TODO error case for unavalable repos or wrong repo url
    import redis
    redis_host = current_app.config["REDIS_HOST"]
    redis_port = current_app.config["REDIS_PORT"]
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    status = r.get(f"repo_status:{url_id}") #there can be no spaces in the string!
    if status is None or status == "failed":
        task = index_repo.delay(url, url_id) # start celery worker on task
    r.set(f"repo_status:{url_id}", "indexing", ex=600)
    r.expire(url_id, 600)  # Optional: timeout in case indexing crashes
    return {"status" : "indexing"}, 202 # 202 means task in progress

@api_bp.route("/status", methods=["POST"])
def status():
    data = request.get_json()
    url_id = data.get("id")

    import redis
    redis_host = current_app.config["REDIS_HOST"]
    redis_port = current_app.config["REDIS_PORT"]
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    status = r.get(f"repo_status:{url_id}")
    if not status:
        n_status = "not"
    elif status == "indexing":
        n_status = "indexing"
    elif status == "done":
        n_status = "done"
    elif status == "failed":
        n_status = "failed"
    return {"status" : n_status}, 200