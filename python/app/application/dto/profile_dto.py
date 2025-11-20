from pydantic import BaseModel
from typing import Optional


class ProfileData(BaseModel):
    username: str
    bio: Optional[str] = None
    image: Optional[str] = None
    following: bool = False
    
    class Config:
        from_attributes = True
