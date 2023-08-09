
model_names_map = {'mpnet': {'embedding':'HuggingFaceEmbeddings', 'name':'sentence-transformers/multi-qa-mpnet-base-dot-v1'},  # 0
                   # 1
                   'e5': {'embedding':'HuggingFaceEmbeddings', 'name':'intfloat/multilingual-e5-large'},
                   # 2
                   'shibing624': {'embedding':'HuggingFaceEmbeddings', 'name':'shibing624/text2vec-base-chinese'},
                   # 4
                   'GanymedeNil':  {'embedding':'HuggingFaceEmbeddings', 'name': 'GanymedeNil/text2vec-large-chinese'},
                   # 5
                   'all_mpnet':  {'embedding':'HuggingFaceEmbeddings', 'name': 'sentence-transformers/all-mpnet-base-v2'},
                   # 6
                   'shibing_paraphrase': {'embedding':'HuggingFaceEmbeddings', 'name': 'shibing624/text2vec-base-chinese-paraphrase'},
                   'luotuo': {'embedding':'HuggingFaceEmbeddings', 'name':'silk-road/luotuo-bert-medium'},
                   'fin-bert': {'embedding':'HuggingFaceEmbeddings', 'name': 'D:\\models\\FinBERT_L-12_H-768_A-12_pytorch\\FinBERT_L-12_H-768_A-12_pytorch'},
                   # 8
                   'qa_mpnet':  {'embedding':'HuggingFaceEmbeddings', 'name': 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'},
                   'my-184': {'embedding':'HuggingFaceEmbeddings', 'name': 'C:\\Users\\zhang\\dev\\sentence-transformers\\output\\training_paraphrases_hfl-chinese-lert-large-2023-07-18_21-11-13\\184'},
                   'my-799': {'embedding':'HuggingFaceEmbeddings', 'name': 'C:\\Users\\zhang\\dev\\sentence-transformers\\output\\training_paraphrases_hfl-chinese-lert-large-2023-07-21_14-13-37\\799'},
                   'bge':  {'embedding':'HuggingFaceEmbeddings', 'name': 'BAAI/bge-large-zh'},
                   }

data_input_dir = ['./dw/test_1', './dw/survey_qa_pairs']
