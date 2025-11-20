from pydantic import BaseModel
from datetime import datetime
from app.application.dto.profile_dto import ProfileData


class CommentData(BaseModel):
    id: str
    body: str
    created_at: datetime
    updated_at: datetime
    author: ProfileData
    
    class Config:
        from_attributes = True


class NewCommentParam(BaseModel):
    body: str
