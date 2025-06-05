# app/routes/api.py
from flask import Blueprint, request, jsonify, current_app
import requests



from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.core.indices import VectorStoreIndex, load_index_from_storage
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from datetime import datetime

#qdrant_host = current_app.config["QDRANT_HOST"] # TODO do it like this
QDRANT_URL = "http://qdrant:6333" #TODO make it like this using network in compose "http://qdrant:6333"

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

    print("setting embed model")


    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.core import Settings
    #TODO move this outside
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )
    # Set the embedding model, we do this only once when we start the backend
    print("creating index")
    # Create index
    client = QdrantClient(host="qdrant", port=6333)  # qdrant is the name of the qdrant service
    print("t")
    vector_store = QdrantVectorStore(collection_name=url_id, client=client)
    print("tt")
    storage_context = StorageContext.from_defaults(vector_store= vector_store)
    print("ttt")
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    print("retrieving")
    # Retrieve
    retriever_engine = index.as_retriever(similarity_top_k=5) #TODO we can just choose 3 here
    print("tttt")
    retrieval_results = retriever_engine.retrieve(query)
    print("ttttt")
    #retrieved_drawing_ids = [n.node.metadata["file_path"] for n in retrieval_results]
    results = [n.node.text for n in retrieval_results]

    print("querying llm")
    # Query LLM
    context = ""
    for result in results:
        context += result
    from groq import Groq

    client = Groq() # TODO this loads api key from env variable so we have to set it
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"{context}\n {query}"
            }
        ]
    )
    print(completion.choices[0].message.content)
    print("returning")
    return {"response": completion.choices[0].message.content}, 200