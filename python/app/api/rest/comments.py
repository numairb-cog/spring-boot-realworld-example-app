from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.application.dto.comment_dto import NewCommentParam, CommentData
from app.application.services.comment_service import CommentService
from app.application.services.article_query_service import ArticleQueryService
from app.api.dependencies import (
    get_comment_service,
    get_article_query_service,
    get_current_user_id,
    get_current_user_id_required
)

router = APIRouter()


class NewCommentRequest(BaseModel):
    comment: NewCommentParam


class CommentResponse(BaseModel):
    comment: CommentData


class CommentsResponse(BaseModel):
    comments: List[CommentData]


@router.post("/articles/{slug}/comments", response_model=CommentResponse, status_code=201)
def create_comment(
    slug: str,
    request: NewCommentRequest,
    current_user_id: str = Depends(get_current_user_id_required),
    comment_service: CommentService = Depends(get_comment_service),
    article_query_service: ArticleQueryService = Depends(get_article_query_service)
):
    article = article_query_service.find_by_slug(slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    from app.core.repositories.article_repository import ArticleRepository
    from app.api.dependencies import get_article_repository
    from sqlalchemy.orm import Session
    from app.infrastructure.db.session import get_db
    
    db = next(get_db())
    article_repo = get_article_repository(db)
    article_domain = article_repo.find_by_slug(slug)
    
    if not article_domain:
        raise HTTPException(status_code=404, detail="Article not found")
    
    comment = comment_service.create_comment(article_domain.id, request.comment, current_user_id)
    comment_data = comment_service.find_by_id(comment.id, current_user_id)
    if not comment_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve comment data")
    return CommentResponse(comment=comment_data)


@router.get("/articles/{slug}/comments", response_model=CommentsResponse)
def get_comments(
    slug: str,
    current_user_id: Optional[str] = Depends(get_current_user_id),
    comment_service: CommentService = Depends(get_comment_service),
    article_query_service: ArticleQueryService = Depends(get_article_query_service)
):
    article = article_query_service.find_by_slug(slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    from app.core.repositories.article_repository import ArticleRepository
    from app.api.dependencies import get_article_repository
    from sqlalchemy.orm import Session
    from app.infrastructure.db.session import get_db
    
    db = next(get_db())
    article_repo = get_article_repository(db)
    article_domain = article_repo.find_by_slug(slug)
    
    if not article_domain:
        raise HTTPException(status_code=404, detail="Article not found")
    
    comments = comment_service.find_by_article_id(article_domain.id, current_user_id)
    return CommentsResponse(comments=comments)


@router.delete("/articles/{slug}/comments/{comment_id}", status_code=204)
def delete_comment(
    slug: str,
    comment_id: str,
    current_user_id: str = Depends(get_current_user_id_required),
    comment_service: CommentService = Depends(get_comment_service)
):
    comment_data = comment_service.find_by_id(comment_id)
    if not comment_data:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    success = comment_service.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return None
