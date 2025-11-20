from dataclasses import dataclass


@dataclass
class ArticleFavorite:
    user_id: str
    article_id: str
