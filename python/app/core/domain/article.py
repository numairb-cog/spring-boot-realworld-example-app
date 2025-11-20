from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid
import re


@dataclass
class Tag:
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Article:
    title: str
    description: str
    body: str
    user_id: str
    tags: List[Tag]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    slug: str = field(default="")
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.slug:
            self.slug = self.to_slug(self.title)
    
    @staticmethod
    def to_slug(title: str) -> str:
        return re.sub(r"[&\[\uFE30-\uFFA0]|'|\"|\s|\?|,|\.+", "-", title.lower())
    
    def update(self, title: Optional[str] = None, description: Optional[str] = None, 
               body: Optional[str] = None) -> None:
        if title and title.strip():
            self.title = title
            self.slug = self.to_slug(title)
            self.updated_at = datetime.utcnow()
        if description and description.strip():
            self.description = description
            self.updated_at = datetime.utcnow()
        if body and body.strip():
            self.body = body
            self.updated_at = datetime.utcnow()
