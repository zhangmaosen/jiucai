import os
import shutil
import json
import re
from langchain.schema.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def clear_line(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)

model_names = ['sentence-transformers/multi-qa-mpnet-base-dot-v1', # 0
               'intfloat/multilingual-e5-large', # 1
               'shibing624/text2vec-base-chinese', # 2
               'hkunlp/instructor-large', # 3
               'GanymedeNil/text2vec-large-chinese', # 4
               'sentence-transformers/all-mpnet-base-v2', # 5
               'shibing624/text2vec-base-chinese-paraphrase', # 6
               'silk-road/luotuo-bert-medium', # 7
               ]

model_select = 7
is_new_test = True

data_dir = "./dw/splited_docs/summary_splits"

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
persist_directory = 'summary_db_'+model_name_pre+'_embedding'
if is_new_test :
    if not os.path.exists(parent_path):
        os.mkdir(parent_path)
    
    
    persist_directory = parent_path + persist_directory
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)



db = Chroma.from_texts([''],hf, persist_directory=persist_directory)


data_part_num = 0
summary_num = 0 
docs = []
docs_size = 500
is_need_split = True

text_splitter = RecursiveCharacterTextSplitter(separators=['\u3000\u3000','\n'],chunk_size=400, chunk_overlap=50)
for root, ds, fs in os.walk(data_dir):

    for f in fs:
        data_part_num += 1
        
        fullname = os.path.join(root, f)
        

        with open(fullname, mode='r', encoding='utf8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                summary_num += 1

                j_data = json.loads(line)
                data = j_data

                title = data["title"]
                file_name = data["file_name"]

                content = data["content"]
                if content is None:
                    #print(f'document is {code} {name} \'s content is null', end='\r')
                    content = 'None'

                if is_need_split:
                    doc = Document(page_content=content,
                                metadata={
                                    "title":title,
                                    "file_name":file_name
                                })
                    split_docs = text_splitter.split_documents([doc])
                    docs += split_docs

                else:
                    doc = Document(page_content=content,
                                metadata={
                                    "title":title,
                                    "file_name":file_name
                                })
                
                    docs.append(doc)

                if summary_num % docs_size == 0:
                    print(f'load {data_part_num}th  doc, name is {fullname}')
                    print(f'insert {summary_num}th summary to db')
                    
                    db.add_documents(docs)
                    db.persist()
                    docs=[]


db.add_documents(docs)
db.persist()

