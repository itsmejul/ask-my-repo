
from urllib.parse import urlparse
import hashlib
from git import Repo 
from pathlib import Path
import os

def clone_repo(repo_url: str, target_dir: str):
    Repo.clone_from(repo_url, target_dir)

def temp_repo_path(repo_key: str) -> str:
    return Path(__file__).resolve().parent / "temp" / repo_key



from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.core.indices import VectorStoreIndex, load_index_from_storage
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from datetime import datetime

def read_directory_documents(path):
    from llama_index.core import SimpleDirectoryReader
    documents = SimpleDirectoryReader(path, recursive=True).load_data()
    return documents

def create_index(documents, url_id):    

    collection_name = url_id
    print("a")
    qdrant_host = os.getenv("QDRANT_HOST") #current_app.config["QDRANT_HOST"]
    qdrant_port = os.getenv("QDRANT_PORT") # current_app.config["QDRANT_PORT"]
    #qdrant_host = "qdrant"
    #qdrant_port = "6333"
    client = QdrantClient(host=qdrant_host, port=qdrant_port) #TODO load from config
    print("e")
    print(client.get_collections())
    #client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    # Create the index
    vector_store = QdrantVectorStore(collection_name=collection_name, client=client)
    print("ee")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    print("ff")
    index = VectorStoreIndex(documents, storage_context=storage_context)
    print("gg")
    # Store index in directory
    #index.storage_context.persist(persist_dir=f"./storage/{collection_name}")

# TODO uncouple vector index creation and document index creation