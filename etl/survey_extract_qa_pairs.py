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

data_split_num = 0
survey_num = 0 
docs = []


parent_dir = "./dw/"
is_need_extract = True
split_buckets_cnt = 25
split_out_dir = './survey_qa_pairs/'

data_input_dir = "./dw/survey_contents"

#text_splitter = RecursiveCharacterTextSplitter(separators=['\r\n\r\n','\n\n','\r\n'],chunk_size=400, chunk_overlap=50)

data_out_dir = parent_dir + split_out_dir

if os.path.exists(data_out_dir):
    shutil.rmtree(data_out_dir)
os.mkdir(data_out_dir)

for root, ds, fs in os.walk(data_input_dir):

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
                data = j_data["result"]["data"][0]

                code = data["SECURITY_CODE"]

                name = data["SECURITY_NAME_ABBR"]

                content = data["CONTENT"]

                date = data["NOTICE_DATE"]

                if content is None:
                    #print(f'document is {code} {name} \'s content is null', end='\r')
                    content = 'None'

                if is_need_extract:
                    
                        
                    ret = re.findall('([^。!]+?\?)([^\?]*[。!])', content) # extract question and answer pair
                    content_re = []
                    for i in range(len(ret)):
                        content_re.append(ret[i])

                    if len(content_re) == 0:
                        content_re.append(['None','None'])
                    
                    for question,answer in content_re:
                        #s_c = name + ":" + s_c
                        doc = Document(page_content=answer,
                                metadata={
                                    'question':question,
                                    "code":code,
                                    "name":name,
                                    'date':date,
                                })
                        
                        
                        
                        docs.append(doc)
                else:
                    doc = Document(page_content=content,
                                metadata={
                                    "code":code,
                                    "name":name
                                })
                
                    docs.append(doc)

                suffix = str(survey_num % split_buckets_cnt)+'.json'

                data_out_filename =  data_out_dir+'/split_' + suffix

                with open(data_out_filename, 'a+', encoding='utf8') as out_f:
                    for i_doc in docs:
                        tmp = {"page_content":i_doc.page_content, "metadata":i_doc.metadata}
                        
                        out_f.writelines(json.dumps(tmp,ensure_ascii=False) + "\n")
                
                docs = []
                print(f'load {data_split_num}th  doc, name is {fullname}', end='\r')

                    



