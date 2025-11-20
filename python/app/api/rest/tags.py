from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from app.core.repositories.article_repository import ArticleRepository
from app.api.dependencies import get_article_repository

router = APIRouter()


class TagsResponse(BaseModel):
    tags: List[str]


@router.get("/tags", response_model=TagsResponse)
def get_tags(
    article_repository: ArticleRepository = Depends(get_article_repository)
):
    tags = article_repository.get_all_tags()
    return TagsResponse(tags=tags)
