import gradio as gr
import torch
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA
from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma

from langchain.embeddings import HuggingFaceEmbeddings

from langchain.embeddings import HuggingFaceInstructEmbeddings

summary_db = None
survey_db = None

summary_embedding = None
survey_embedding = None

def update(*args):
    global summary_embedding, survey_embedding
    global summary_db, survey_db 

    [summary_db_selected, survey_db_selected] = args

    model_names_map = {'mpnet':'sentence-transformers/multi-qa-mpnet-base-dot-v1', # 0
              'e5': 'intfloat/multilingual-e5-large', # 1
              'shibing624': 'shibing624/text2vec-base-chinese', # 2
               'GanymedeNil':'GanymedeNil/text2vec-large-chinese', # 4
               'all_mpnet':'sentence-transformers/all-mpnet-base-v2', # 5
               'shibing_paraphrase':'shibing624/text2vec-base-chinese-paraphrase', # 6
               'luotuo':'silk-road/luotuo-bert-medium',
               'qa_mpnet':'sentence-transformers/multi-qa-mpnet-base-cos-v1', # 8
               'my-184':'C:\\Users\\zhang\\dev\\sentence-transformers\\output\\training_paraphrases_hfl-chinese-lert-large-2023-07-18_21-11-13\\184',
    }
    

    summary_model_name = model_names_map[summary_db_selected]
    survey_model_name = model_names_map[survey_db_selected]

    if 'summary_embedding' in locals() or 'summary_embedding' in globals():
        print('clear gpu embedding memory')
        del summary_embedding
        torch.cuda.empty_cache()

    print(f'summary db is  {summary_model_name}, survey db is {survey_model_name} selected!')

    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}

    summary_embedding = HuggingFaceEmbeddings(
        model_name=summary_model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    survey_embedding = HuggingFaceEmbeddings(
        model_name=survey_model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    relative_path = './'

    summary_db_name_pre = summary_model_name.split('/')[-1]
    if survey_db_selected == 'my-184':
        survey_db_name_pre = 'my-184'
    else:
        survey_db_name_pre = survey_model_name.split('/')[-1]

    
    parent_path = './embedding_dbs/'
    summary_persist_directory = parent_path + 'summary_db_'+summary_db_name_pre+'_embedding'
    summary_persist_directory = relative_path + summary_persist_directory

    survey_persist_directory = parent_path + 'survey_db_'+survey_db_name_pre+'_embedding'
    survey_persist_directory = relative_path + survey_persist_directory


    summary_db = Chroma(persist_directory=summary_persist_directory, embedding_function=summary_embedding,collection_metadata={"hnsw:space": "cosine"})
    survey_db =  Chroma(persist_directory=survey_persist_directory, embedding_function=survey_embedding,collection_metadata={"hnsw:space": "cosine"})
    return f'load model {summary_model_name} in {summary_persist_directory} \n load model {survey_model_name} in {survey_persist_directory}'
    
def greet(query):
    summary = summary_db.similarity_search_with_score(query, k=2)
    survey = survey_db.similarity_search_with_score(query, k=3)
    print(f'query is {query}, result is {summary} \n {survey}')
    return summary+survey 


update('shibing_paraphrase','my-184')


with gr.Blocks() as demo:
    model_names = ['e5','shibing624','mpnet', 'GanymedeNil', 'shibing_paraphrase', 'luotuo','qa_mpnet', 'my-184']
    summary_db_selected = gr.Dropdown(model_names, value="shibing_paraphrase", label="研报摘要数据库")
    survey_db_selected = gr.Dropdown(model_names, value="shibing_paraphrase", label="公司调研记录数据库")


    refresh_button = gr.Button('load db')
    refresh_button.click(fn=update,inputs=[summary_db_selected,survey_db_selected], outputs=gr.TextArea(lines=1))
    with gr.Row():
        gr.Interface(fn=greet, inputs="text", outputs=["text",
                                                           "text",
                                                           "text",
                                                           "text",
                                                           "text",])
if 'demo' in locals() or 'demo' in globals():
    demo.close()
demo.launch(server_name="0.0.0.0",share=True)  