import os
import re
import json
from pathlib import Path

project_name = 'jiucai'


program_name = os.path.basename(__file__)
program_path = os.path.dirname(__file__)
 
print('File name :    ', program_name)
print('Directory Name:     ', program_path)

data_input_path = program_path + '/../../dw//survey_qa_pairs/'
#test_data_input_path = program_path + '/../../dw/test/survey_contents/'
data_output_path = program_path + '/../../dw/corpus/'

question_pattern = '(.*\?)((?:.|\n)*)'
corpus_output_name = data_output_path + 'stock_qa.txt'

with open(corpus_output_name, 'w+', encoding='utf8') as out_file:
    for root, ds, fs in os.walk(data_input_path):

        for f in fs:
            
            fullname = os.path.join(root, f)
            
            with open(fullname, 'r', encoding='utf8') as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    
                    data_json_str = json.loads(line)
                    answer = data_json_str["page_content"]
                    question = data_json_str["metadata"]["question"]
                   
                    answer = answer.replace("\t",'')
                    question = question.replace("\t", '')

                    answer = re.sub("[\n\r]", '', answer)
                    question = re.sub("[\n\r]", '', question)
                    out_file.writelines(question+'\t'+answer+'\n')
            
out_file.close()