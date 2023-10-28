from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uuid, random

# fastapiを実行
app = FastAPI()

# Agent情報を辞書形式で保持
agent_dict = {}

# BaseModelをインポート
from models import OnAction

# 自然言語モデルに対する処理
@app.post("/on_action")
async def on_action(req: OnAction):

    # 空文字列を受け取るとuuidを新規発行
    if req.client_uuid == "":
        client_uuid = uuid.uuid4()
        agent_dict[client_uuid] = None

    # (仮の処理)
    random_bool = random.choice([True, False])
    response_data = {"is_same_topic": random_bool}

    return JSONResponse(content=response_data, status_code=200)
