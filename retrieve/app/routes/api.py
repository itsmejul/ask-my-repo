# app/routes/api.py
from flask import Blueprint, request, jsonify, current_app
import requests

from app.utils import within_budget


from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.core.indices import VectorStoreIndex, load_index_from_storage
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from datetime import datetime


api_bp = Blueprint("api", __name__)

@api_bp.route("/health", methods=["POST"])
def health():
    return {"status": "hello"}, 200

@api_bp.route("/repo/retrieve", methods=["POST"])
def retrieve_repo():
    print("entering retrieve method")
    data = request.get_json()
    url_id = data.get("id")
    query = data.get("query")

    # Set the embedding model, we do this only once when we start the backend
    print("creating index")

    qdrant_host = current_app.config["QDRANT_HOST"]
    qdrant_port = current_app.config["QDRANT_PORT"]
    # Create index
    client = QdrantClient(host=qdrant_host, port=qdrant_port)
    vector_store = QdrantVectorStore(collection_name=url_id, client=client)
    storage_context = StorageContext.from_defaults(vector_store= vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    print("retrieving")
    # Retrieve

    n_retrieval_results = current_app.config["N_RETRIEVAL_RESULTS"]
    retriever_engine = index.as_retriever(similarity_top_k=n_retrieval_results) #TODO we can just choose 3 here
    retrieval_results = retriever_engine.retrieve(query)
    #retrieved_drawing_ids = [n.node.metadata["file_path"] for n in retrieval_results]
    results = [n.node.text for n in retrieval_results]

    print("querying llm")
    # Query LLM
    context = ""
    for result in results:
        context += result
    from groq import Groq

    is_within_budget = within_budget()

    if is_within_budget:
        llm_model_name = current_app.config["LLM_MODEL_NAME"] # TODO explain this config
        print(llm_model_name) 
        client = Groq()
        completion = client.chat.completions.create(
            model=llm_model_name,
            messages=[
                {
                    "role": "user",
                    "content": f"{context}\n {query}"
                }
            ]
        )
        print(completion.choices[0].message.content)
        return {"response": completion.choices[0].message.content}, 200
    else:
        return {"response" : "Max number of Requests reached. Try again later."}, 200