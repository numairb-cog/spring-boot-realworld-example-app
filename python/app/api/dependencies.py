from typing import Optional
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_db
from app.infrastructure.security.jwt_service import JwtService
from app.infrastructure.security.password_hasher import PasswordHasher
from app.core.repositories.user_repository import UserRepository
from app.core.repositories.article_repository import ArticleRepository
from app.core.repositories.comment_repository import CommentRepository
from app.core.repositories.favorite_repository import FavoriteRepository
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.article_repository_impl import ArticleRepositoryImpl
from app.infrastructure.repositories.comment_repository_impl import CommentRepositoryImpl
from app.infrastructure.repositories.favorite_repository_impl import FavoriteRepositoryImpl
from app.application.services.user_service import UserService
from app.application.services.user_query_service import UserQueryService
from app.application.services.article_service import ArticleCommandService
from app.application.services.article_query_service import ArticleQueryService
from app.application.services.profile_query_service import ProfileQueryService
from app.application.services.comment_service import CommentService


def get_jwt_service() -> JwtService:
    return JwtService()


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(db)


def get_article_repository(db: Session = Depends(get_db)) -> ArticleRepository:
    return ArticleRepositoryImpl(db)


def get_comment_repository(db: Session = Depends(get_db)) -> CommentRepository:
    return CommentRepositoryImpl(db)


def get_favorite_repository(db: Session = Depends(get_db)) -> FavoriteRepository:
    return FavoriteRepositoryImpl(db)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher)
) -> UserService:
    return UserService(user_repository, password_hasher)


def get_user_query_service(db: Session = Depends(get_db)) -> UserQueryService:
    return UserQueryService(db)


def get_article_command_service(
    article_repository: ArticleRepository = Depends(get_article_repository)
) -> ArticleCommandService:
    return ArticleCommandService(article_repository)


def get_article_query_service(db: Session = Depends(get_db)) -> ArticleQueryService:
    return ArticleQueryService(db)


def get_profile_query_service(db: Session = Depends(get_db)) -> ProfileQueryService:
    return ProfileQueryService(db)


def get_comment_service(
    comment_repository: CommentRepository = Depends(get_comment_repository),
    db: Session = Depends(get_db)
) -> CommentService:
    return CommentService(comment_repository, db)


def get_current_user_id(
    authorization: Optional[str] = Header(None),
    jwt_service: JwtService = Depends(get_jwt_service)
) -> Optional[str]:
    if not authorization:
        return None
    
    if not authorization.startswith("Token "):
        return None
    
    token = authorization[6:]
    user_id = jwt_service.get_sub_from_token(token)
    return user_id


def get_current_user_id_required(
    authorization: Optional[str] = Header(None),
    jwt_service: JwtService = Depends(get_jwt_service)
) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    if not authorization.startswith("Token "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    token = authorization[6:]
    user_id = jwt_service.get_sub_from_token(token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user_id
