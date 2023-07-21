import gradio as gr
import torch
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA
from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma

from langchain.embeddings import HuggingFaceEmbeddings

with gr.Blocks as demo:
    with gr.Row():
        gr.Number()
        gr.Button()

demo.start()