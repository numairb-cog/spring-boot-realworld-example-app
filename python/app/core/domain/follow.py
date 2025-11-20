from dataclasses import dataclass


@dataclass
class FollowRelation:
    user_id: str
    follow_id: str
