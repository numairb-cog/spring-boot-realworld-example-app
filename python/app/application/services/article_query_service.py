from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.application.dto.article_dto import ArticleData, ArticleDataList, Page
from app.application.dto.profile_dto import ProfileData
from app.infrastructure.db.models import ArticleModel, UserModel, ArticleFavoriteModel, FollowModel, TagModel, article_tags


class ArticleQueryService:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_slug(self, slug: str, current_user_id: Optional[str] = None) -> Optional[ArticleData]:
        article_model = self.db.query(ArticleModel).filter(ArticleModel.slug == slug).first()
        if not article_model:
            return None
        return self._to_article_data(article_model, current_user_id)
    
    def find_recent_articles(
        self, 
        page: Page, 
        tag: Optional[str] = None,
        author: Optional[str] = None,
        favorited: Optional[str] = None,
        current_user_id: Optional[str] = None
    ) -> ArticleDataList:
        query = self.db.query(ArticleModel)
        
        if tag:
            query = query.join(article_tags).join(TagModel).filter(TagModel.name == tag)
        
        if author:
            query = query.join(UserModel, ArticleModel.user_id == UserModel.id).filter(UserModel.username == author)
        
        if favorited:
            user = self.db.query(UserModel).filter(UserModel.username == favorited).first()
            if user:
                query = query.join(ArticleFavoriteModel).filter(ArticleFavoriteModel.user_id == user.id)
        
        total = query.count()
        articles = query.order_by(desc(ArticleModel.created_at)).offset(page.offset).limit(page.limit).all()
        
        article_data_list = [self._to_article_data(article, current_user_id) for article in articles]
        return ArticleDataList(articles=article_data_list, articles_count=total)
    
    def find_user_feed(self, user_id: str, page: Page) -> ArticleDataList:
        query = self.db.query(ArticleModel).join(
            FollowModel, ArticleModel.user_id == FollowModel.follow_id
        ).filter(FollowModel.user_id == user_id)
        
        total = query.count()
        articles = query.order_by(desc(ArticleModel.created_at)).offset(page.offset).limit(page.limit).all()
        
        article_data_list = [self._to_article_data(article, user_id) for article in articles]
        return ArticleDataList(articles=article_data_list, articles_count=total)
    
    def _to_article_data(self, article_model: ArticleModel, current_user_id: Optional[str] = None) -> ArticleData:
        author = self.db.query(UserModel).filter(UserModel.id == article_model.user_id).first()
        
        favorited = False
        if current_user_id:
            fav = self.db.query(ArticleFavoriteModel).filter(
                ArticleFavoriteModel.user_id == current_user_id,
                ArticleFavoriteModel.article_id == article_model.id
            ).first()
            favorited = fav is not None
        
        favorites_count = self.db.query(func.count(ArticleFavoriteModel.article_id)).filter(
            ArticleFavoriteModel.article_id == article_model.id
        ).scalar() or 0
        
        following = False
        if current_user_id and author:
            follow = self.db.query(FollowModel).filter(
                FollowModel.user_id == current_user_id,
                FollowModel.follow_id == author.id
            ).first()
            following = follow is not None
        
        author_profile = ProfileData(
            username=author.username,
            bio=author.bio,
            image=author.image,
            following=following
        ) if author else ProfileData(username="unknown", following=False)
        
        tag_list = [tag.name for tag in article_model.tags]
        
        return ArticleData(
            slug=article_model.slug,
            title=article_model.title,
            description=article_model.description,
            body=article_model.body,
            tag_list=tag_list,
            created_at=article_model.created_at,
            updated_at=article_model.updated_at,
            favorited=favorited,
            favorites_count=favorites_count,
            author=author_profile
        )
