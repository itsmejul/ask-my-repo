
from urllib.parse import urlparse
import hashlib
from git import Repo 
from pathlib import Path

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

    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.core import Settings

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )
    collection_name = url_id
    print("a")
    client = QdrantClient(host="qdrant", port=6333) #TODO load from config
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