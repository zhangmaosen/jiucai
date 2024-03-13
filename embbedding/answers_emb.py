import ray
from typing import Dict, List
import numpy as np
import pyarrow.json as pajson


from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from transformers import AutoModel
from llama_index.core.node_parser import  SentenceSplitter #SimpleNodeParser
from llama_index.core.schema import Node
from llama_index.core.schema import Document
import pandas as pd
import pyarrow as pa
import warnings
import pandas as pd
import copy
from llama_index.core.schema import TextNode, NodeRelationship, RelatedNodeInfo

import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from chromadb.errors import DuplicateIDError
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)

block_size = 10 << 25 # Set block size to 300MB
ds = ray.data.read_json('/home/userroot/dev/jiucai/crawl/stock_report/survey_contents' ,read_options=pajson.ReadOptions(block_size=block_size))

class EmbedNodes:
    def __init__(self):
        import os
        #os.environ['HTTPS_PROXY'] = 'http://100.109.83.118:808/'
        self.embedding_model = HuggingFaceEmbeddings(model_name='/data/models/bge-large-zh')

    #列存储的方式
    def __call__(self, data_batch: Dict[str, np.ndarray]) -> Dict[str, List[Node]]:
        nodes = []
        summaries = []
        answers_batch = data_batch['result']
        for a in answers_batch:
            for aa in a['data']:

                #t = aa['CONTENT'] 
                text_list =  [str(value) for value in aa.values()]
                joined_text = ','.join(text_list)
                node = TextNode(text=str(joined_text))
                nodes.append(node)
                summaries.append(str(joined_text))
                break
        
        embeddings = self.embedding_model.embed_documents(summaries)
        assert len(nodes) == len(embeddings)

        for node, embedding in zip(nodes, embeddings):
            node.embedding = embedding
        return {"embedded_nodes": nodes}
    
embeds = ds.map_batches(EmbedNodes, concurrency=4, num_gpus=1, batch_size=400)
stock_docs_nodes = []
title_dict = {}
for row in embeds.iter_rows():
    node:Node = row["embedded_nodes"]
    if not node.id_ in title_dict:
        title_dict[node.id_] = True
        assert node.embedding is not None
        stock_docs_nodes.append(node)

print(f'text embedding finished! goto load into chromadb.')

Settings.llm = Ollama(model="deepseek-llm:67b", request_timeout=120.0)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="/data/models/bge-large-zh"
)

# initialize client, setting path to save data
db = chromadb.PersistentClient(path="./stock_db")

# create collection
chroma_collection = db.get_or_create_collection("qa_base")

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


#create your index
try:
    index = VectorStoreIndex(
        nodes=stock_docs_nodes, storage_context=storage_context
    )
except DuplicateIDError:
    print("duplicat id, ignore it!")

print(f'load into db done!')
ray.shutdown()