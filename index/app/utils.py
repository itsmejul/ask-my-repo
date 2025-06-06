from urllib.parse import urlparse
import hashlib
from pathlib import Path
import os
from datetime import datetime

from git import Repo 
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.core.indices import VectorStoreIndex, load_index_from_storage
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

def clone_repo(repo_url: str, target_dir: str):
    '''
    Clone contents of github repository into local directory
    '''
    Repo.clone_from(repo_url, target_dir)

def temp_repo_path(repo_key: str) -> str:
    '''
    Construct path for temporary storage of contents of cloned repository.
    '''
    return Path(__file__).resolve().parent / "temp" / repo_key

def read_directory_documents(path):
    '''
    Read documents in specified path and return as list of documents.
    '''
    from llama_index.core import SimpleDirectoryReader
    documents = SimpleDirectoryReader(path, recursive=True).load_data()
    return documents

def create_index(documents, url_id):
    '''
    Create Collection in Qdrant with specified documents and id.
    '''
    collection_name = url_id
    qdrant_host = os.getenv("QDRANT_HOST") 
    qdrant_port = os.getenv("QDRANT_PORT") 
    client = QdrantClient(host=qdrant_host, port=qdrant_port) 
    print(client.get_collections())
    vector_store = QdrantVectorStore(collection_name=collection_name, client=client)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(documents, storage_context=storage_context)