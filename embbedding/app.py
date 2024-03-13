import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteria, StoppingCriteriaList, TextIteratorStreamer
from threading import Thread

import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from chromadb.errors import DuplicateIDError
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.llm = Ollama(model="qwen:7b", request_timeout=120.0)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="/data/models/bge-large-zh"
)

# initialize client, setting path to save data
db = chromadb.PersistentClient(path="/home/userroot/dev/jiucai/embbedding/stock_db")

# create collection
chroma_collection = db.get_or_create_collection("stock_summary")

print(chroma_collection.peek())
# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_vector_store(
    vector_store
)
query_engine = index.as_query_engine(
    similarity_top_k = 10
)
response = query_engine.query('测试')

print(response)