#セルの区切りは#のみの行で表します
##################################################
#環境の統一
import locale
locale.getpreferredencoding = lambda: "UTF-8"
# !pip uninstall lida -y
# !pip uninstall llmx -y
# !pip uninstall tensorflow-probability -y


requirements = [
"fastapi",
"uvicorn",
"torch",
"transformers",
"sentencepiece",
"accelerate",
"bitsandbytes",
"scipy",
"flet",
"plyer",
"simpleaudio",
]

for x in requirements:
    # !pip install $x

#colabではエラー
#!pip install git+https://github.com/kivy/pyobjus/zipball/master


##################################################

# fastAPIのインストール
# !pip install fastapi nest-asyncio pyngrok uvicorn

##################################################]

#LLMのインストール
# ! pip install transformers sentencepiece accelerate bitsandbytes

##################################################
#############################
#         models.py         #
#############################
from pydantic import BaseModel

class OnAction(BaseModel):
    client_uuid: str
    search_word: str
    page_content: str


#################################################
#############################
#            LLM.py         #
#############################
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
class Agent:
    tokenizer = AutoTokenizer.from_pretrained(
        "rinna/bilingual-gpt-neox-4b-instruction-ppo",
        use_fast=False
    )
    def __init__(self):
        self.model = AutoModelForCausalLM.from_pretrained(
            "rinna/bilingual-gpt-neox-4b-instruction-ppo",
            load_in_8bit=True,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        self.query_history = []
        self.answer_history = []

    def on_user_action(self, user_action: OnAction):
        try :
            # プロンプトの準備
            prompt = """
これから、あるプログラマーが開発の中で行き詰まった時に検索した言葉を「検索ワード:」に続いて、また、その検索ワードの下で訪れたwebページの冒頭を「訪問ページ冒頭:」の形式で与えます。これらを順次与えますが、直前までと同じ課題について検索している時は”True”を、検索して解決しようとしている課題が切り替わった時には”False”を出力してください。以下に、例をいくつか示します。私が与える文章の先頭には”Q:”を、あなたが出力する文章の先頭には”A:”をつけています。この入力に対してあなたは”True”または”False”以外を出力していはいけません。
Q:検索ワード:chrome.tabs.onUpdated.addListener
A:True

Q:検索ワード:mozilla tabs.onUpdated
A:False

Q:検索ワード:chrome拡張 作り方
A:True
です。では、始めます。
"""
            for i in range(len(self.query_history)):
                prompt += "Q:検索ワード:" + self.query_history[i] + "\nA:" + str(self.answer_history[i]) + "\n\n"
            prompt += "Q:検索ワード:" + user_action.search_word + "A:"
            # 推論の実行
            token_ids = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
            with torch.no_grad():
                output_ids = self.model.generate(
                    token_ids.to(self.model.device),
                    max_new_tokens=512,
                    do_sample=True,
                    temperature=1.0,
                    top_p=0.85,
                    pad_token_id=self.tokenizer.pad_token_id,
                    bos_token_id=self.tokenizer.bos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            output = self.tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])

            is_same_topic = True if output == "True</s>" else False
            self.query_history.append(user_action.search_word)
            self.answer_history.append(is_same_topic)
            return is_same_topic
        except :
            print("LLM error!")
            self.query_history.append(user_action.search_word)
            self.answer_history.append(is_same_topic)
            return False


##################################################
#############################
#         server.py         #
#############################

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid, random
# from LLM import Agent

# fastapiを実行
app = FastAPI()

# CORSミドルウェアを有効にする
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agent情報を辞書形式で保持
agent_dict = {}

# BaseModelをインポート
#from models import OnAction

# 自然言語モデルに対する処理
@app.post("/on_action")
async def on_action(req: OnAction):
    client_uuid_str = str(req.client_uuid)
    # 空文字列を受け取るとuuidを新規発行
    if client_uuid_str == "":
        client_uuid_str = str(uuid.uuid4())
        agent_dict[client_uuid_str] = Agent()


    is_same_topic = agent_dict[client_uuid_str].on_user_action(req)
    response_data = {"is_same_topic": is_same_topic, "client_uuid": client_uuid_str}

    return JSONResponse(content=response_data, status_code=200)


##################################################
import nest_asyncio
from pyngrok import ngrok
import uvicorn

ngrok_tunnel = ngrok.connect(8000)
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port=8000)