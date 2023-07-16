import os
import shutil
import json
import re
from langchain.schema.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

model_names = ['sentence-transformers/multi-qa-mpnet-base-dot-v1', # 0
               'intfloat/multilingual-e5-large', # 1
               'shibing624/text2vec-base-chinese', # 2
               'hkunlp/instructor-large', # 3
               'GanymedeNil/text2vec-large-chinese', # 4
               'sentence-transformers/all-mpnet-base-v2', # 5
               'shibing624/text2vec-base-chinese-paraphrase', # 6
               'silk-road/luotuo-bert-medium', # 7
               'sentence-transformers/multi-qa-mpnet-base-cos-v1', # 8
               ]

model_select = 8
is_new_test = True



model_name = model_names[model_select]
model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings': True}

# hf = HuggingFaceEmbeddings(
#     model_name=model_name,
#     model_kwargs=model_kwargs,
#     encode_kwargs=encode_kwargs
# )


hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
from langchain.vectorstores import Chroma

model_name_pre = model_name.split('/')[-1]
parent_path = './embedding_dbs/'
persist_directory = 'survey_db_'+model_name_pre+'_embedding'
if is_new_test :
    if not os.path.exists(parent_path):
        os.mkdir(parent_path)
    
    
    persist_directory = parent_path + persist_directory
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)



db = Chroma.from_texts([''],hf, persist_directory=persist_directory)


data_split_num = 0
survey_num = 0 
docs = []
docs_size = 8000

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

data_dir = "./dw/splited_docs/survey_splits"
for root, ds, fs in os.walk(data_dir):

    for f in fs:
        data_split_num += 1
        
        fullname = os.path.join(root, f)
        

        with open(fullname, mode='r', encoding='utf8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                survey_num += 1

                j_data = json.loads(line)
                doc = Document(page_content=j_data['page_content'],
                                metadata=j_data['metadata'])
                        

                docs.append(doc)

                if survey_num % docs_size == 0:
                    print(f'load {data_split_num}th  doc, name is {fullname}')
                    print(f'insert {survey_num}th survey to db')
                    
                    db.add_documents(docs)
                    db.persist()
                    docs=[]


db.add_documents(docs)
db.persist()

