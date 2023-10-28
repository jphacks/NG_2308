from pydantic import BaseModel

class OnAction(BaseModel):
    client_uuid: str
    search_word: str
    page_content: str
