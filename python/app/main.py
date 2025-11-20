from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from ariadne import load_schema_from_path, make_executable_schema, graphql
from ariadne.asgi import GraphQL
from sqlalchemy.orm import Session
from app.api.rest import users, user, articles, comments, profiles, tags, favorites
from app.api.graphql.resolvers import query, mutation
from app.infrastructure.db.models import Base
from app.infrastructure.db.session import engine, get_db
from app.api.dependencies import (
    get_jwt_service,
    get_password_hasher,
    get_user_repository,
    get_article_repository,
    get_comment_repository,
    get_favorite_repository,
    get_user_service,
    get_user_query_service,
    get_article_command_service,
    get_article_query_service,
    get_profile_query_service,
    get_comment_service
)
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RealWorld API - Python")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(user.router, prefix="/api", tags=["user"])
app.include_router(articles.router, prefix="/api", tags=["articles"])
app.include_router(comments.router, prefix="/api", tags=["comments"])
app.include_router(profiles.router, prefix="/api", tags=["profiles"])
app.include_router(tags.router, prefix="/api", tags=["tags"])
app.include_router(favorites.router, prefix="/api", tags=["favorites"])


schema_path = os.path.join(os.path.dirname(__file__), "api/graphql/schema.graphqls")
type_defs = load_schema_from_path(schema_path)
schema = make_executable_schema(type_defs, query, mutation)


async def get_graphql_context(request: Request) -> dict:
    db = next(get_db())
    jwt_service = get_jwt_service()
    
    current_user_id = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Token "):
        token = auth_header[6:]
        current_user_id = jwt_service.get_sub_from_token(token)
    
    return {
        "request": request,
        "db": db,
        "current_user_id": current_user_id,
        "jwt_service": jwt_service,
        "password_hasher": get_password_hasher(),
        "user_repository": get_user_repository(db),
        "article_repository": get_article_repository(db),
        "comment_repository": get_comment_repository(db),
        "favorite_repository": get_favorite_repository(db),
        "user_service": get_user_service(get_user_repository(db), get_password_hasher()),
        "user_query_service": get_user_query_service(db),
        "article_service": get_article_command_service(get_article_repository(db)),
        "article_query_service": get_article_query_service(db),
        "profile_query_service": get_profile_query_service(db),
        "comment_service": get_comment_service(get_comment_repository(db), db)
    }


graphql_app = GraphQL(schema, context_value=get_graphql_context)
app.mount("/graphql", graphql_app)


@app.get("/")
def root():
    return {"message": "RealWorld API - Python implementation"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
