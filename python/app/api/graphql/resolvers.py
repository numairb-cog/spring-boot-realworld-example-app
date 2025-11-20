from typing import Any, Optional
from ariadne import QueryType, MutationType, ObjectType
from app.application.dto.user_dto import RegisterParam, LoginParam, UpdateUserParam
from app.application.dto.article_dto import NewArticleParam, UpdateArticleParam, Page
from app.application.dto.comment_dto import NewCommentParam
from app.core.domain.follow import FollowRelation
from app.core.domain.favorite import ArticleFavorite


query = QueryType()
mutation = MutationType()
article_type = ObjectType("Article")
profile_type = ObjectType("Profile")
user_type = ObjectType("User")


@query.field("me")
def resolve_me(obj: Any, info: Any) -> Optional[dict]:
    context = info.context
    current_user_id = context.get("current_user_id")
    if not current_user_id:
        return None
    
    user_query_service = context["user_query_service"]
    jwt_service = context["jwt_service"]
    
    user_data = user_query_service.find_by_id(current_user_id)
    if not user_data:
        return None
    
    from app.core.domain.user import User
    user = User(id=user_data.id, email=user_data.email, username=user_data.username, password="")
    token = jwt_service.to_token(user)
    
    return {
        "email": user_data.email,
        "username": user_data.username,
        "token": token,
        "profile": {
            "username": user_data.username,
            "bio": user_data.bio,
            "image": user_data.image,
            "following": False
        }
    }


@query.field("article")
def resolve_article(obj: Any, info: Any, slug: str) -> Optional[dict]:
    context = info.context
    current_user_id = context.get("current_user_id")
    article_query_service = context["article_query_service"]
    
    article_data = article_query_service.find_by_slug(slug, current_user_id)
    if not article_data:
        return None
    
    return {
        "slug": article_data.slug,
        "title": article_data.title,
        "description": article_data.description,
        "body": article_data.body,
        "tagList": article_data.tag_list,
        "createdAt": article_data.created_at.isoformat(),
        "updatedAt": article_data.updated_at.isoformat(),
        "favorited": article_data.favorited,
        "favoritesCount": article_data.favorites_count,
        "author": {
            "username": article_data.author.username,
            "bio": article_data.author.bio,
            "image": article_data.author.image,
            "following": article_data.author.following
        }
    }


@query.field("articles")
def resolve_articles(obj: Any, info: Any, **kwargs) -> dict:
    context = info.context
    current_user_id = context.get("current_user_id")
    article_query_service = context["article_query_service"]
    
    first = kwargs.get("first", 20)
    offset = 0
    
    page = Page(offset=offset, limit=first)
    result = article_query_service.find_recent_articles(
        page=page,
        tag=kwargs.get("withTag"),
        author=kwargs.get("authoredBy"),
        favorited=kwargs.get("favoritedBy"),
        current_user_id=current_user_id
    )
    
    edges = []
    for article_data in result.articles:
        edges.append({
            "cursor": article_data.slug,
            "node": {
                "slug": article_data.slug,
                "title": article_data.title,
                "description": article_data.description,
                "body": article_data.body,
                "tagList": article_data.tag_list,
                "createdAt": article_data.created_at.isoformat(),
                "updatedAt": article_data.updated_at.isoformat(),
                "favorited": article_data.favorited,
                "favoritesCount": article_data.favorites_count,
                "author": {
                    "username": article_data.author.username,
                    "bio": article_data.author.bio,
                    "image": article_data.author.image,
                    "following": article_data.author.following
                }
            }
        })
    
    return {
        "edges": edges,
        "pageInfo": {
            "hasNextPage": len(edges) >= first,
            "hasPreviousPage": False,
            "startCursor": edges[0]["cursor"] if edges else None,
            "endCursor": edges[-1]["cursor"] if edges else None
        }
    }


@query.field("profile")
def resolve_profile(obj: Any, info: Any, username: str) -> Optional[dict]:
    context = info.context
    current_user_id = context.get("current_user_id")
    profile_query_service = context["profile_query_service"]
    
    profile = profile_query_service.find_by_username(username, current_user_id)
    if not profile:
        return None
    
    return {
        "profile": {
            "username": profile.username,
            "bio": profile.bio,
            "image": profile.image,
            "following": profile.following
        }
    }


@query.field("tags")
def resolve_tags(obj: Any, info: Any) -> list:
    context = info.context
    article_repository = context["article_repository"]
    return article_repository.get_all_tags()


@mutation.field("createUser")
def resolve_create_user(obj: Any, info: Any, input: dict) -> dict:
    context = info.context
    user_service = context["user_service"]
    user_query_service = context["user_query_service"]
    jwt_service = context["jwt_service"]
    
    try:
        param = RegisterParam(
            email=input["email"],
            username=input["username"],
            password=input["password"]
        )
        user = user_service.create_user(param)
        user_data = user_query_service.find_by_id(user.id)
        token = jwt_service.to_token(user)
        
        return {
            "user": {
                "email": user_data.email,
                "username": user_data.username,
                "token": token,
                "profile": {
                    "username": user_data.username,
                    "bio": user_data.bio,
                    "image": user_data.image,
                    "following": False
                }
            }
        }
    except ValueError as e:
        return {
            "message": str(e),
            "errors": [{"key": "body", "value": [str(e)]}]
        }


@mutation.field("login")
def resolve_login(obj: Any, info: Any, email: str, password: str) -> dict:
    context = info.context
    user_repository = context["user_repository"]
    user_query_service = context["user_query_service"]
    jwt_service = context["jwt_service"]
    password_hasher = context["password_hasher"]
    
    user = user_repository.find_by_email(email)
    if not user or not password_hasher.verify(password, user.password):
        raise Exception("Invalid email or password")
    
    user_data = user_query_service.find_by_id(user.id)
    token = jwt_service.to_token(user)
    
    return {
        "user": {
            "email": user_data.email,
            "username": user_data.username,
            "token": token,
            "profile": {
                "username": user_data.username,
                "bio": user_data.bio,
                "image": user_data.image,
                "following": False
            }
        }
    }


@mutation.field("updateUser")
def resolve_update_user(obj: Any, info: Any, changes: dict) -> dict:
    context = info.context
    current_user_id = context.get("current_user_id")
    if not current_user_id:
        raise Exception("Authentication required")
    
    user_service = context["user_service"]
    user_query_service = context["user_query_service"]
    jwt_service = context["jwt_service"]
    
    param = UpdateUserParam(**changes)
    user = user_service.update_user(current_user_id, param)
    user_data = user_query_service.find_by_id(user.id)
    token = jwt_service.to_token(user)
    
    return {
        "user": {
            "email": user_data.email,
            "username": user_data.username,
            "token": token,
            "profile": {
                "username": user_data.username,
                "bio": user_data.bio,
                "image": user_data.image,
                "following": False
            }
        }
    }


@mutation.field("createArticle")
def resolve_create_article(obj: Any, info: Any, input: dict) -> dict:
    context = info.context
    current_user_id = context.get("current_user_id")
    if not current_user_id:
        raise Exception("Authentication required")
    
    article_service = context["article_service"]
    article_query_service = context["article_query_service"]
    
    param = NewArticleParam(
        title=input["title"],
        description=input["description"],
        body=input["body"],
        tag_list=input.get("tagList", [])
    )
    article = article_service.create_article(param, current_user_id)
    article_data = article_query_service.find_by_slug(article.slug, current_user_id)
    
    return {
        "article": {
            "slug": article_data.slug,
            "title": article_data.title,
            "description": article_data.description,
            "body": article_data.body,
            "tagList": article_data.tag_list,
            "createdAt": article_data.created_at.isoformat(),
            "updatedAt": article_data.updated_at.isoformat(),
            "favorited": article_data.favorited,
            "favoritesCount": article_data.favorites_count,
            "author": {
                "username": article_data.author.username,
                "bio": article_data.author.bio,
                "image": article_data.author.image,
                "following": article_data.author.following
            }
        }
    }


@mutation.field("followUser")
def resolve_follow_user(obj: Any, info: Any, username: str) -> dict:
    context = info.context
    current_user_id = context.get("current_user_id")
    if not current_user_id:
        raise Exception("Authentication required")
    
    user_repository = context["user_repository"]
    profile_query_service = context["profile_query_service"]
    
    user_to_follow = user_repository.find_by_username(username)
    if not user_to_follow:
        raise Exception("User not found")
    
    existing_relation = user_repository.find_relation(current_user_id, user_to_follow.id)
    if not existing_relation:
        relation = FollowRelation(user_id=current_user_id, follow_id=user_to_follow.id)
        user_repository.save_relation(relation)
    
    profile = profile_query_service.find_by_username(username, current_user_id)
    
    return {
        "profile": {
            "username": profile.username,
            "bio": profile.bio,
            "image": profile.image,
            "following": profile.following
        }
    }


@mutation.field("favoriteArticle")
def resolve_favorite_article(obj: Any, info: Any, slug: str) -> dict:
    context = info.context
    current_user_id = context.get("current_user_id")
    if not current_user_id:
        raise Exception("Authentication required")
    
    article_repository = context["article_repository"]
    favorite_repository = context["favorite_repository"]
    article_query_service = context["article_query_service"]
    
    article = article_repository.find_by_slug(slug)
    if not article:
        raise Exception("Article not found")
    
    existing_favorite = favorite_repository.find(current_user_id, article.id)
    if not existing_favorite:
        favorite = ArticleFavorite(user_id=current_user_id, article_id=article.id)
        favorite_repository.save(favorite)
    
    article_data = article_query_service.find_by_slug(slug, current_user_id)
    
    return {
        "article": {
            "slug": article_data.slug,
            "title": article_data.title,
            "description": article_data.description,
            "body": article_data.body,
            "tagList": article_data.tag_list,
            "createdAt": article_data.created_at.isoformat(),
            "updatedAt": article_data.updated_at.isoformat(),
            "favorited": article_data.favorited,
            "favoritesCount": article_data.favorites_count,
            "author": {
                "username": article_data.author.username,
                "bio": article_data.author.bio,
                "image": article_data.author.image,
                "following": article_data.author.following
            }
        }
    }
