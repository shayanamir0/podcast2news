from pydantic import BaseModel
from typing import List, Optional

class NewsArticle(BaseModel):
    title: str
    content: str
    key_quote: str

class TranscriptResponse(BaseModel):
    success: bool
    transcript: str
    url: str
    error: Optional[str] = None

class NewsResponse(BaseModel):
    success: bool
    articles: List[NewsArticle]
    session_id: str
    url: str
    error: Optional[str] = None 