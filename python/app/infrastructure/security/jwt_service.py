import jwt
from datetime import datetime, timedelta
from typing import Optional
from app.config import settings
from app.core.domain.user import User


class JwtService:
    def __init__(self):
        self.secret = settings.jwt_secret
        self.session_time = settings.jwt_session_time
        self.algorithm = "HS512"
    
    def to_token(self, user: User) -> str:
        exp = datetime.utcnow() + timedelta(seconds=self.session_time)
        payload = {
            "sub": user.id,
            "exp": exp
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)
    
    def get_sub_from_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload.get("sub")
        except Exception:
            return None
