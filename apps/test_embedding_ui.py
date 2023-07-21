import gradio as gr
import models_map
import test_embedding_ctrl as emb
test_num = range(2)
db1 = any
db2 = any
def query(query):
    global db1, db2 
    out_puts = []
    out_puts += emb.query(query, db1)
    out_puts += emb.query(query, db2)

    return out_puts


def load_data(model_1,  input_data_dir ):
    
    print(f'input_data_dir is {input_data_dir}')
    emb.load_data2db(model_1, input_data_dir)
    print(f'load db {model_1} complete')


def load_db(db_1, db_2, db_dir):
    global db1, db2 
    print(f'load db {db_1} into memory')
    db1 = emb.load_db_from_dir(db_1, db_dir + db_1)

    print(f'load db {db_2} into memory')
    db2 = emb.load_db_from_dir(db_2, db_dir + db_2)

with gr.Blocks() as demo:
    with gr.Tab("对比查询"):

        with gr.Row():
            with gr.Column():
                db_1 = gr.Dropdown(choices=list(models_map.model_names_map.keys()), label=f'1号数据库')
            with gr.Column():
                db_2 = gr.Dropdown(choices=list(models_map.model_names_map.keys()), label=f'2号数据库')
        with gr.Row():
            db_dir = gr.Dropdown(choices=['./embedding_dbs/test_db/'], label=f'数据库所在路径')
            load_db_btn = gr.Button()

        with gr.Row():
            query_input = gr.Textbox()
            query_btn = gr.Button()
            
        with gr.Row():

                with gr.Column():
                    with gr.Row():
                        t_1_1 = gr.Textbox()
                        t_1_2 =gr.Textbox()
                        t_1_3 = gr.Textbox()
                with gr.Column():
                    with gr.Row():
                        t_2_1 = gr.Textbox()
                        t_2_2 = gr.Textbox()
                        t_2_3 = gr.Textbox()

    
    with gr.Tab("创建测试数据库"):
        
        with gr.Row():
            model_name_1 = gr.Dropdown(choices=list(models_map.model_names_map.keys()), label=f'选择数据库对应的embedding模型')

        input_data_dir = gr.Dropdown(choices=models_map.data_input_dir, label='测试数据库所在目录')
        load_data_btn = gr.Button()

    #model_load_btn.click()
    load_data_btn.click(fn=load_data, inputs=[model_name_1, input_data_dir], outputs=[gr.Textbox()])
    load_db_btn.click(fn=load_db, inputs=[db_1, db_2, db_dir ], outputs=[gr.Textbox()])
    query_btn.click(fn=query,inputs=[query_input], outputs=[t_1_1, t_1_2, t_1_3, t_2_1, t_2_2, t_2_3])
demo.launch()