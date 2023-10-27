from fastapi import FastAPI


app = FastAPI()

# 適当なダミーのエンドポイント
@app.post("/test/{id}")
async def test(id: str,):
    print(f"got request {id}")
