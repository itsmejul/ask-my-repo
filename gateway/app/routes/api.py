# app/routes/main.py
from flask import Blueprint, request, jsonify, current_app
import requests
from app.utils import hash_repo_url, exists_repo

api_bp = Blueprint("api", __name__)

@api_bp.route("/repo/query", methods=["POST"])
def query_repo():
    data = request.get_json()
    url = data.get("url")
    query = data.get("query")
    url_id = hash_repo_url(url)

    retrieve_host = current_app.config["RETRIEVE_HOST"]
    retrieve_port = current_app.config["RETRIEVE_PORT"]
    retrieve_url = "http://" + retrieve_host + ":" + str(retrieve_port)

    index_host = current_app.config["INDEX_HOST"]
    index_port = current_app.config["INDEX_PORT"]
    index_url = "http://" + index_host + ":" + str(index_port)
    exists = exists_repo(url_id)
    if exists:
        res = requests.post(retrieve_url + "/repo/retrieve", json = {"id": url_id, "query" : query})
    else:
        res = requests.post(index_url + "/repo/index", json = {"id": url_id, "query" : query}) 
    return res.json()

@api_bp.route("/start-indexing", methods=["POST"])
def start_indexing():
    data = request.get_json()
    url = data.get("url")
    url_id = hash_repo_url(url)
    exists = exists_repo(url_id)
    index_host = current_app.config["INDEX_HOST"]
    index_port = current_app.config["INDEX_PORT"]
    index_url = "http://" + index_host + ":" + str(index_port)
    if not exists:
        res = requests.post(index_url + "/index", json={"url" : url, "id" : url_id})
    return {"status" : "indexing"}, 202 

@api_bp.route("/status", methods=["POST"])
def status():
    data = request.get_json()
    url = data.get("url") # TODO make this into utils method extract_id_from_request
    url_id = hash_repo_url(url)

    exists = exists_repo(url_id)
    index_host = current_app.config["INDEX_HOST"]
    index_port = current_app.config["INDEX_PORT"]
    index_url = "http://" + index_host + ":" + str(index_port)
    if not exists:
        res = requests.post(index_url + "/status", json={"id" : url_id})
        status = res.json().get("status")
    else:
        status = "done"
    return {"status" : status}, 200