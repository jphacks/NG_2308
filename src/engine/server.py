from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import judge

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

# BaseModelをインポート
from model import OnPageOpen, OnGoogleSearch

search_word = ""
client_uuid = ""

# 検索内容とページ内容をセットにして悩み続けているか判定
@app.post("/on_page_open")
async def on_page_open(req: OnPageOpen):
    global search_word
    global client_uuid
    client_uuid = judge.judge(client_uuid, search_word, req.content)
    print(req.content)
    response_data = {"message": "This is a successful response."}
    return JSONResponse(content=response_data, status_code=200)

# 検索ワードを保存
@app.post("/on_google_search")
async def on_google_search(req: OnGoogleSearch):
    global search_word
    search_word = req.query
    print(req.query)
    response_data = {"message": "This is a successful response."}
    return JSONResponse(content=response_data, status_code=200)
