from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


article_tags = Table(
    'article_tags',
    Base.metadata,
    Column('article_id', String(255), ForeignKey('articles.id')),
    Column('tag_id', String(255), ForeignKey('tags.id'))
)


class UserModel(Base):
    __tablename__ = 'users'
    
    id = Column(String(255), primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    image = Column(String(511), nullable=True)


class ArticleModel(Base):
    __tablename__ = 'articles'
    
    id = Column(String(255), primary_key=True)
    user_id = Column(String(255), ForeignKey('users.id'), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    body = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tags = relationship('TagModel', secondary=article_tags, backref='articles')


class TagModel(Base):
    __tablename__ = 'tags'
    
    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)


class ArticleFavoriteModel(Base):
    __tablename__ = 'article_favorites'
    
    article_id = Column(String(255), ForeignKey('articles.id'), primary_key=True)
    user_id = Column(String(255), ForeignKey('users.id'), primary_key=True)


class FollowModel(Base):
    __tablename__ = 'follows'
    
    user_id = Column(String(255), ForeignKey('users.id'), primary_key=True)
    follow_id = Column(String(255), ForeignKey('users.id'), primary_key=True)


class CommentModel(Base):
    __tablename__ = 'comments'
    
    id = Column(String(255), primary_key=True)
    body = Column(Text, nullable=True)
    article_id = Column(String(255), ForeignKey('articles.id'), nullable=False)
    user_id = Column(String(255), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
