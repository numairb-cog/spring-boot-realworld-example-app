from pydantic import BaseModel, EmailStr
from typing import Optional


class UserData(BaseModel):
    id: str
    email: str
    username: str
    bio: Optional[str] = None
    image: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserWithToken(BaseModel):
    email: str
    username: str
    bio: Optional[str] = None
    image: Optional[str] = None
    token: str


class RegisterParam(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginParam(BaseModel):
    email: EmailStr
    password: str


class UpdateUserParam(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None
