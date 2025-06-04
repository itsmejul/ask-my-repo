# app/routes/api.py
from flask import Blueprint, request, jsonify
import requests

QDRANT_URL = "http://qdrant:6333" #TODO make it like this using network in compose "http://qdrant:6333"

api_bp = Blueprint("api", __name__)

@api_bp.route("/health", methods=["POST"])
def health():
    return {"status": "hello"}, 200
