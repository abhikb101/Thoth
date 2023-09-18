from llama_index import download_loader
import os
from llama_index.node_parser import SimpleNodeParser
from llama_index import GPTVectorStoreIndex
from llama_index import StorageContext
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.storage.index_store import SimpleIndexStore
from llama_index.vector_stores import SimpleVectorStore
from llama_index import load_index_from_storage, load_indices_from_storage, load_graph_from_storage
import openai
from settings import PINECONE_API_KEY, OPENAI_API_KEY, PINECONE_API_ENV
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY
os.environ['PINECONE_API_ENV'] = PINECONE_API_ENV

openai.api_key = os.environ["OPENAI_API_KEY"]

storage_context = StorageContext.from_defaults(
    docstore=SimpleDocumentStore.from_persist_dir(persist_dir="./database"),
    vector_store=SimpleVectorStore.from_persist_dir(persist_dir="./database"),
    index_store=SimpleIndexStore.from_persist_dir(persist_dir="./database"),
)

index = load_index_from_storage(storage_context) 

query_engine = index.as_query_engine()

