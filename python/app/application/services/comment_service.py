from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.comment import Comment
from app.core.repositories.comment_repository import CommentRepository
from app.application.dto.comment_dto import CommentData, NewCommentParam
from app.application.dto.profile_dto import ProfileData
from app.infrastructure.db.models import UserModel, FollowModel


class CommentService:
    def __init__(self, comment_repository: CommentRepository, db: Session):
        self.comment_repository = comment_repository
        self.db = db
    
    def create_comment(self, article_id: str, param: NewCommentParam, user_id: str) -> Comment:
        comment = Comment(
            body=param.body,
            article_id=article_id,
            user_id=user_id
        )
        return self.comment_repository.save(comment)
    
    def delete_comment(self, comment_id: str) -> bool:
        comment = self.comment_repository.find_by_id(comment_id)
        if not comment:
            return False
        self.comment_repository.remove(comment)
        return True
    
    def find_by_article_id(self, article_id: str, current_user_id: Optional[str] = None) -> List[CommentData]:
        comments = self.comment_repository.find_by_article_id(article_id)
        return [self._to_comment_data(comment, current_user_id) for comment in comments]
    
    def find_by_id(self, comment_id: str, current_user_id: Optional[str] = None) -> Optional[CommentData]:
        comment = self.comment_repository.find_by_id(comment_id)
        if not comment:
            return None
        return self._to_comment_data(comment, current_user_id)
    
    def _to_comment_data(self, comment: Comment, current_user_id: Optional[str] = None) -> CommentData:
        author = self.db.query(UserModel).filter(UserModel.id == comment.user_id).first()
        
        following = False
        if current_user_id and author:
            follow = self.db.query(FollowModel).filter(
                FollowModel.user_id == current_user_id,
                FollowModel.follow_id == author.id
            ).first()
            following = follow is not None
        
        author_profile = ProfileData(
            username=author.username if author else "unknown",
            bio=author.bio if author else None,
            image=author.image if author else None,
            following=following
        )
        
        return CommentData(
            id=comment.id,
            body=comment.body,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            author=author_profile
        )
