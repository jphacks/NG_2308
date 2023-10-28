from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# fastapiを実行
app = FastAPI()

class PageOpen(BaseModel):
    content: str

class GoogleSearch(BaseModel):
    query: str

@app.post("/on_page_open")
async def on_page_open(item: PageOpen):
    print(item.content)
    response_data = {"message": "This is a successful response."}
    return JSONResponse(content=response_data, status_code=200)

@app.post("/on_google_search")
async def on_google_search(item: GoogleSearch):
    print(item.query)
    response_data = {"message": "This is a successful response."}
    return JSONResponse(content=response_data, status_code=200)