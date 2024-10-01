import gradio as gr
import gacha_simulator as gsimu
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

def create_gradio_interface():
    with gr.Blocks() as demo:

        # ガチャを（普通に）ひく
        with gr.Column():
            gr.Markdown("# ガチャをひく")

            # 1連、10連用ボタン
            with gr.Row():
                gacha_btn = gr.Button("ガチャをひく！(1回)")
                gacha_btn_ten = gr.Button("ガチャをひく！(10回, ☆2確定)")

            # 出力用テキストボックス
            output = gr.Textbox(label="ガチャ結果")

            # ボタン押下のイベントリスナー
            gacha_btn.click(fn=gsimu.gacha_once, outputs=output)
            gacha_btn_ten.click(fn=gsimu.gacha_ten_time, outputs=output)
        
        #特定のキャラがひけるまでガチャを回す
        with gr.Column():
            gr.Markdown("# キャラをひく")

            # キャラ名入力用テキストボックス
            input = gr.Textbox(label="ひきたいキャラ")

            # 実行ボタン
            gacha_btn_chara = gr.Button("キャラが出るまでひく！")

            # 出力（ガチャ結果、回した回数）テキストボックス
            output_chara_result = gr.Textbox(label="ガチャ結果")
            output_chara_count = gr.Textbox(label="回した回数")

            #ボタン押下のイベントリスナー
            gacha_btn_chara.click(
                fn=gsimu.gacha_chara,
                inputs=input,
                outputs=[
                    output_chara_result,
                    output_chara_count
                ]
            )
    
    return demo

# Gradioインターフェースの作成
demo = create_gradio_interface()
demo.queue()

# FastAPIアプリにGradioインターフェースをマウント
gradio_app = gr.mount_gradio_app(app, demo, path="/gacha")

# ルートパスにアクセスしたときに/gachaにリダイレクト
@app.get("/")
async def root():
    return RedirectResponse('/gacha')

# /gachaパスへのアクセスをGradioアプリにハンドオーバー
app.mount("/gacha", gradio_app)

# uvicorn webui:app --host 0.0.0.0