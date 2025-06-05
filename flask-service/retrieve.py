

import os
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

from utils import clone_repo, hash_repo_url, sanitize_repo_url, temp_repo_path

def init():
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY")
    if not QDRANT_HOST:
        raise ValueError("Missing QDRANT_HOST")
    if not QDRANT_PORT:
        raise ValueError("Missing QDRANT_PORT")

    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.core import Settings

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )
    # Set the embedding model, we do this only once when we start the backend


import subprocess
from pathlib import Path





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

    documents = SimpleDirectoryReader("./temp", recursive=True).load_data()
    return documents




def create_index(documents, repo_url):

    collection_name = hash_repo_url(repo_url)
    print("a")
    client = QdrantClient(host="localhost", port=6333)
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


def query_index(query, repo_url):
    collection_name = hash_repo_url(repo_url)
    client = QdrantClient(host="localhost", port=6333)
    #client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    # Create the index
    vector_store = QdrantVectorStore(collection_name=collection_name, client=client)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    #storage_context = StorageContext.from_defaults(persist_dir=f"./storage/{collection_name}") # Load qdrant inde here
    #index = load_index_from_storage(storage_context)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    #query="What are the methods that make up the genetic algorithm?"
    #query = "How did they center the div?"
    #query = "how does the game loop work?"
    
    retriever_engine = index.as_retriever(similarity_top_k=10)
    retrieval_results = retriever_engine.retrieve(query)
    retrieved_drawing_ids = [n.node.metadata["file_path"] for n in retrieval_results]
    print(retrieved_drawing_ids)
    print([n.node.metadata["file_path"] for n in retrieval_results][:3])
    top_3_results = [n.node.text for n in retrieval_results][:3]
    return top_3_results

def query_llm(retrieval_results, query):
    context = ""
    for result in retrieval_results:
        context += result
    from groq import Groq
    client = Groq() # Loads the API key automatically from the environment variable
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
    return completion.choices[0].message.content

def clone_and_read(repo_url, query):
    clone_repo(repo_url=repo_url, target_dir="./temp")

    documents = read_directory_documents("./temp")
    print("Creating index...")
    create_index(documents, repo_url)
    print("querying index...")
    retrieval_results = query_index(query, repo_url)
    print("querying llm...")
    llm_response = query_llm(query, retrieval_results)
    
    subprocess.run(["rm", "-rf", "./temp"])
    print("returning...")
    return llm_response