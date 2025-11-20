from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.application.dto.profile_dto import ProfileData


class ArticleData(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tag_list: List[str] = []
    created_at: datetime
    updated_at: datetime
    favorited: bool = False
    favorites_count: int = 0
    author: ProfileData
    
    class Config:
        from_attributes = True


class NewArticleParam(BaseModel):
    title: str
    description: str
    body: str
    tag_list: Optional[List[str]] = []


class UpdateArticleParam(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None


class ArticleDataList(BaseModel):
    articles: List[ArticleData]
    articles_count: int


class Page(BaseModel):
    offset: int = 0
    limit: int = 20
