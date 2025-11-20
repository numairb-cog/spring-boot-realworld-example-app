from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.domain.comment import Comment
from app.core.repositories.comment_repository import CommentRepository
from app.infrastructure.db.models import CommentModel


class CommentRepositoryImpl(CommentRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, comment: Comment) -> Comment:
        comment_model = CommentModel(
            id=comment.id,
            body=comment.body,
            article_id=comment.article_id,
            user_id=comment.user_id,
            created_at=comment.created_at,
            updated_at=comment.updated_at
        )
        self.db.add(comment_model)
        self.db.commit()
        self.db.refresh(comment_model)
        return self._to_domain(comment_model)
    
    def find_by_id(self, comment_id: str) -> Optional[Comment]:
        comment_model = self.db.query(CommentModel).filter(CommentModel.id == comment_id).first()
        return self._to_domain(comment_model) if comment_model else None
    
    def find_by_article_id(self, article_id: str) -> List[Comment]:
        comment_models = self.db.query(CommentModel).filter(CommentModel.article_id == article_id).all()
        return [self._to_domain(cm) for cm in comment_models]
    
    def remove(self, comment: Comment) -> None:
        self.db.query(CommentModel).filter(CommentModel.id == comment.id).delete()
        self.db.commit()
    
    def _to_domain(self, comment_model: CommentModel) -> Comment:
        return Comment(
            id=comment_model.id,
            body=comment_model.body,
            article_id=comment_model.article_id,
            user_id=comment_model.user_id,
            created_at=comment_model.created_at,
            updated_at=comment_model.updated_at
        )
