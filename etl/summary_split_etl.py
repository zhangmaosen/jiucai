import os
import scrapy
from scrapy.selector import Selector
import json
import shutil
import hashlib
import re

def clear_line(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)

i = 1
parent_dir = './dw/'
json_summary_dir = 'splited_docs/summary_splits/'

out_dir = parent_dir + json_summary_dir
isExist = os.path.exists(out_dir)
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs(out_dir)
   print(f"The new directory {out_dir} is created!")
else:
    shutil.rmtree(out_dir)
    os.makedirs(out_dir)

data_dir = 'summaries'
input_dir = parent_dir + data_dir
for root, ds, fs in os.walk(input_dir):

    for f in fs:
        
        i += 1

        fullname = os.path.join(root, f)
        #print(fullname)

        content = ''
        with open(fullname, encoding='utf8') as file:
            r = str(file.readlines())
            #print(r)
            body = Selector(text=r)
            title = body.css('.c-title h1::text').get()
            #print(f'title is {title}')
            content = (body.css('.ctx-content').css('p::text').getall())
            content = '\n'.join(content)
            date = re.findall('AP(\d{8})', f)[0]
            #print(f'content is {content}')
            j = json.dumps({'title':title, 'content':content, 'file_name':fullname, 'date':date}, ensure_ascii=False)

            file_name = f.split('.')[0]+'.json'
            split_name = 'split_' + str(hash(file_name) % 20) + '.jsonl'
            out_f_name = out_dir + split_name
            print(f'etl {i}th doc')
            print(f'load into {out_f_name}')
            clear_line(n=2)
            with open(out_f_name,'a',encoding='utf8') as out_f:
                out_f.writelines(j+'\n')
        
