from models_map import model_names_map
from langchain.vectorstores import Chroma
from langchain.schema.document import Document
import os
import json
import shutil
from langchain.embeddings import HuggingFaceEmbeddings

def query(query, db:Chroma):
    return db.similarity_search_with_score(query, k=3)

def load_data2db(model_name, input_data_dir, db_dir='./embedding_dbs/test_db/', device_type='cuda', batch_size = 5000, is_append = False):
    '''
    输入数据的格式采用 {
        page_content:{}
        metadata:{}
        }
    '''
    db_dir = db_dir +  model_name
    if not is_append :
        if os.path.exists(db_dir):
            shutil.rmtree(db_dir)
        os.mkdir(db_dir)

    
    model = model_names_map[model_name]
    
    model_kwargs = {'device': device_type}
    encode_kwargs = {'normalize_embeddings': True}

    embedding = HuggingFaceEmbeddings(
        model_name=model,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    print(f'db dir is {db_dir}')
    chroma_db = Chroma(persist_directory=db_dir, embedding_function=embedding,collection_metadata={"hnsw:space": "cosine"})

    data_part_num = 0
    data_line_num = 0
    docs = []
    for root, ds, fs in os.walk(input_data_dir):

        for f in fs:
            data_part_num += 1
            
            fullname = os.path.join(root, f)
            print(f'load data from {fullname}')
            
            with open(fullname, mode='r', encoding='utf8') as f:
                
                while True:
                    line = f.readline()
                    data_line_num += 1
                    if not line:
                        break
                    j_data = json.loads(line)
                    content = j_data['page_content']
                    metadata = j_data['metadata']
                    doc = Document(
                        page_content=content,
                        metadata=metadata)
                    
                    docs.append(doc)

                    if data_line_num % batch_size == 0:
                        chroma_db.add_documents(docs)
                        chroma_db.persist()
                        docs=[]
    
    if docs != []:
        chroma_db.add_documents(docs)
    docs=[]

    chroma_db.persist()
    return chroma_db

def load_db_from_dir(model_name, db_dir, device_type='cpu'):
    model = model_names_map[model_name]
    
    model_kwargs = {'device': device_type}
    encode_kwargs = {'normalize_embeddings': True}

    embedding = HuggingFaceEmbeddings(
        model_name=model,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    chroma_db = Chroma(persist_directory=db_dir, embedding_function=embedding,collection_metadata={"hnsw:space": "cosine"})

    return chroma_db