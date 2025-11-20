from dataclasses import dataclass, field
from typing import Optional
import uuid


@dataclass
class User:
    email: str
    username: str
    password: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    bio: Optional[str] = None
    image: Optional[str] = None
    
    def update(self, email: Optional[str] = None, username: Optional[str] = None, 
               password: Optional[str] = None, bio: Optional[str] = None, 
               image: Optional[str] = None) -> None:
        if email and email.strip():
            self.email = email
        if username and username.strip():
            self.username = username
        if password and password.strip():
            self.password = password
        if bio is not None:
            self.bio = bio
        if image is not None:
            self.image = image
