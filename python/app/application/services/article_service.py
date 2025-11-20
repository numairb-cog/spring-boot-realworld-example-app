from typing import Optional
from app.core.domain.article import Article, Tag
from app.core.repositories.article_repository import ArticleRepository
from app.application.dto.article_dto import NewArticleParam, UpdateArticleParam


class ArticleCommandService:
    def __init__(self, article_repository: ArticleRepository):
        self.article_repository = article_repository
    
    def create_article(self, param: NewArticleParam, user_id: str) -> Article:
        tags = [Tag(name=tag_name) for tag_name in (param.tag_list or [])]
        article = Article(
            title=param.title,
            description=param.description,
            body=param.body,
            user_id=user_id,
            tags=tags
        )
        return self.article_repository.save(article)
    
    def update_article(self, slug: str, param: UpdateArticleParam) -> Optional[Article]:
        article = self.article_repository.find_by_slug(slug)
        if not article:
            return None
        
        article.update(
            title=param.title,
            description=param.description,
            body=param.body
        )
        return self.article_repository.save(article)
    
    def delete_article(self, slug: str) -> bool:
        article = self.article_repository.find_by_slug(slug)
        if not article:
            return False
        self.article_repository.remove(article)
        return True
