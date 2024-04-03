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

Settings.llm = Ollama(model="qwen:72b-chat", request_timeout=360.0, )
Settings.embed_model = HuggingFaceEmbedding(
    model_name="/data/models/bge-large-zh"
)

# initialize client, setting path to save data
db = chromadb.PersistentClient(path="/home/userroot/dev/jiucai/stock_db")

# create collection
chroma_collection = db.get_or_create_collection("qa_base")

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_vector_store(
    vector_store
)
query_engine = index.as_query_engine(
    similarity_top_k = 3
)

import gradio as gr
from IPython.display import Markdown, display
Settings.llm.complete(f'你好',formatted=False,  keep_alive = -1)

def qa(input, input2):
    print(input)
    query_engine = index.as_query_engine(
    similarity_top_k = input2
)
    response = query_engine.query(input+",用中文回答：")
    return (f"{response}")

# demo = gr.Interface(
#     qa,
#     gr.Textbox(placeholder="Enter sentence here..."),
#     ["html"],
#     examples=[
#         ["比亚迪独特的技术优势和企业优势有哪些？"],
#         ["ADC药物的独特优势，和目前成功的产品有哪些？"],
#         ["掌握液冷机房或者服务器技术的厂商有哪些？"]
#     ],
#     title="A股企业资料AI摘要",
#     description="资料库包括了近三年的企业研报摘要和企业调研问答数据，服务运行在二手服务器，响应较慢",
# )


with gr.Blocks() as demo:
    name = gr.Textbox(label="Name")
    gr.Interface(
        qa,
        [gr.Textbox(placeholder="Enter sentence here..."),gr.Slider(2, 5, step =1, value=2, label="抽取资料数量", info="Choose between 2 and 5") ],
        ["html"],
        examples=[
            ["比亚迪独特的技术优势和企业优势有哪些？"],
            ["ADC药物的独特优势，和目前成功的产品有哪些？"],
            ["掌握液冷机房或者服务器技术的厂商有哪些？"]
        ],
        title="A股企业资料AI摘要",
        description="资料库包括了近三年的企业研报摘要和企业调研问答数据，服务运行在二手服务器，响应较慢",
    )
    # output = gr.Textbox(label="Output Box")
    # greet_btn = gr.Button("Greet")
    # greet_btn.click(fn=greet, inputs=name, outputs=output, api_name="greet")


demo.launch(server_name='0.0.0.0')
