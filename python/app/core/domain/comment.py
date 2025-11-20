from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Comment:
    body: str
    article_id: str
    user_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
