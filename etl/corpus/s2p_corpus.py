import os
import re
import json
from pathlib import Path

project_name = 'jiucai'


program_name = os.path.basename(__file__)
program_path = os.path.dirname(__file__)
 
print('File name :    ', program_name)
print('Directory Name:     ', program_path)

data_input_path = program_path + '/../../dw/splited_docs/survey_splits/'
test_data_input_path = program_path + '/../../dw/test/survey_contents/'
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
                    content = data_json_str["page_content"]

                    content = re.sub('[\r\n]', '',content )
                    ret = re.findall(question_pattern, content )
                    
                    if  ret != []:
                        (q, a) = ret[0]


                        #print(f"question is {q}, \n answer is {a}")
                        if q != '' and a != '':
                            out_file.writelines(q+'\t'+a+'\n')
            
out_file.close()