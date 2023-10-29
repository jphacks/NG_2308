from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid, random

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
from models import OnAction

# 自然言語モデルに対する処理
@app.post("/on_action")
async def on_action(req: OnAction):
    client_uuid = req.client_uuid
    # 空文字列を受け取るとuuidを新規発行
    if client_uuid == "":
        client_uuid = str(uuid.uuid4())
        agent_dict[client_uuid] = None

    # (仮の処理)
    random_bool = random.choice([True, False])
    response_data = {"is_same_topic": random_bool, "client_uuid": client_uuid}

    return JSONResponse(content=response_data, status_code=200)
