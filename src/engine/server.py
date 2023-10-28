from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

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

# ページ内容から悩み続けているか判定
@app.post("/on_page_open")
async def on_page_open(req: OnPageOpen):
    print(req.content)
    response_data = {"message": "This is a successful response."}
    return JSONResponse(content=response_data, status_code=200)

# 検索ワードから悩み続けているか判定
@app.post("/on_google_search")
async def on_google_search(req: OnGoogleSearch):
    print(req.query)
    response_data = {"message": "This is a successful response."}
    return JSONResponse(content=response_data, status_code=200)
