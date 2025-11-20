from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.domain.article import Article, Tag
from app.core.repositories.article_repository import ArticleRepository
from app.infrastructure.db.models import ArticleModel, TagModel


class ArticleRepositoryImpl(ArticleRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, article: Article) -> Article:
        article_model = self.db.query(ArticleModel).filter(ArticleModel.id == article.id).first()
        
        tag_models = []
        for tag in article.tags:
            tag_model = self.db.query(TagModel).filter(TagModel.name == tag.name).first()
            if not tag_model:
                tag_model = TagModel(id=tag.id, name=tag.name)
                self.db.add(tag_model)
            tag_models.append(tag_model)
        
        if article_model:
            article_model.title = article.title
            article_model.slug = article.slug
            article_model.description = article.description
            article_model.body = article.body
            article_model.updated_at = article.updated_at
            article_model.tags = tag_models
        else:
            article_model = ArticleModel(
                id=article.id,
                user_id=article.user_id,
                slug=article.slug,
                title=article.title,
                description=article.description,
                body=article.body,
                created_at=article.created_at,
                updated_at=article.updated_at
            )
            article_model.tags = tag_models
            self.db.add(article_model)
        
        self.db.commit()
        self.db.refresh(article_model)
        return self._to_domain(article_model)
    
    def find_by_id(self, article_id: str) -> Optional[Article]:
        article_model = self.db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
        return self._to_domain(article_model) if article_model else None
    
    def find_by_slug(self, slug: str) -> Optional[Article]:
        article_model = self.db.query(ArticleModel).filter(ArticleModel.slug == slug).first()
        return self._to_domain(article_model) if article_model else None
    
    def remove(self, article: Article) -> None:
        self.db.query(ArticleModel).filter(ArticleModel.id == article.id).delete()
        self.db.commit()
    
    def find_tag(self, tag_name: str) -> Optional[Tag]:
        tag_model = self.db.query(TagModel).filter(TagModel.name == tag_name).first()
        return Tag(id=tag_model.id, name=tag_model.name) if tag_model else None
    
    def get_all_tags(self) -> List[str]:
        tags = self.db.query(TagModel.name).distinct().all()
        return [tag[0] for tag in tags]
    
    def _to_domain(self, article_model: ArticleModel) -> Article:
        tags = [Tag(id=tag.id, name=tag.name) for tag in article_model.tags]
        return Article(
            id=article_model.id,
            user_id=article_model.user_id,
            slug=article_model.slug,
            title=article_model.title,
            description=article_model.description,
            body=article_model.body,
            tags=tags,
            created_at=article_model.created_at,
            updated_at=article_model.updated_at
        )
