from typing import Optional
from sqlalchemy.orm import Session
from app.application.dto.profile_dto import ProfileData
from app.infrastructure.db.models import UserModel, FollowModel


class ProfileQueryService:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_username(self, username: str, current_user_id: Optional[str] = None) -> Optional[ProfileData]:
        user = self.db.query(UserModel).filter(UserModel.username == username).first()
        if not user:
            return None
        
        following = False
        if current_user_id:
            follow = self.db.query(FollowModel).filter(
                FollowModel.user_id == current_user_id,
                FollowModel.follow_id == user.id
            ).first()
            following = follow is not None
        
        return ProfileData(
            username=user.username,
            bio=user.bio,
            image=user.image,
            following=following
        )
