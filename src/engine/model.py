from pydantic import BaseModel

class OnPageOpen(BaseModel):
    content: str

class OnGoogleSearch(BaseModel):
    query: str