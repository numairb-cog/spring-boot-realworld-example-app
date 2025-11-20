from typing import Optional
from sqlalchemy.orm import Session
from app.application.dto.user_dto import UserData
from app.infrastructure.db.models import UserModel


class UserQueryService:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, user_id: str) -> Optional[UserData]:
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            return None
        return UserData(
            id=user_model.id,
            email=user_model.email,
            username=user_model.username,
            bio=user_model.bio,
            image=user_model.image
        )
