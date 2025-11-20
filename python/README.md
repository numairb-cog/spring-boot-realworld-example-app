# RealWorld API - Python Implementation

This is a complete Python3 rewrite of the Spring Boot RealWorld Example Application. It implements the [RealWorld](https://github.com/gothinkster/realworld) API specification using FastAPI, SQLAlchemy, and Ariadne (for GraphQL).

## Architecture

This implementation follows the same Domain-Driven Design (DDD) architecture as the original Java application:

- **API Layer** (`app/api/`): REST endpoints (FastAPI) and GraphQL resolvers (Ariadne)
- **Application Layer** (`app/application/`): Application services and DTOs (Pydantic models)
- **Core Layer** (`app/core/`): Domain models and repository interfaces
- **Infrastructure Layer** (`app/infrastructure/`): SQLAlchemy models, repository implementations, JWT service, password hashing

## Features

- **REST API**: Full implementation of RealWorld API endpoints
- **GraphQL API**: Complete GraphQL schema with queries and mutations
- **Authentication**: JWT-based authentication with HS512 algorithm
- **CQRS Pattern**: Separate read and write operations
- **Database**: SQLAlchemy ORM with SQLite (configurable)
- **Testing**: Comprehensive pytest test suite

## Requirements

- Python 3.11+
- pip

## Installation

1. Create a virtual environment:
```bash
cd python
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python init_db.py
```

## Running the Application

### Development Server

```bash
cd python
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Or simply:
```bash
python app/main.py
```

The application will be available at:
- REST API: http://localhost:8080/api
- GraphQL: http://localhost:8080/graphql
- API Documentation: http://localhost:8080/docs

## Running Tests

```bash
cd python
source venv/bin/activate
pytest tests/ -v
```

## API Endpoints

### REST API

- `POST /api/users` - Register a new user
- `POST /api/users/login` - Login user
- `GET /api/user` - Get current user
- `PUT /api/user` - Update current user
- `GET /api/profiles/:username` - Get user profile
- `POST /api/profiles/:username/follow` - Follow user
- `DELETE /api/profiles/:username/follow` - Unfollow user
- `GET /api/articles` - List articles
- `GET /api/articles/feed` - Get user feed
- `GET /api/articles/:slug` - Get article
- `POST /api/articles` - Create article
- `PUT /api/articles/:slug` - Update article
- `DELETE /api/articles/:slug` - Delete article
- `POST /api/articles/:slug/favorite` - Favorite article
- `DELETE /api/articles/:slug/favorite` - Unfavorite article
- `GET /api/articles/:slug/comments` - Get comments
- `POST /api/articles/:slug/comments` - Add comment
- `DELETE /api/articles/:slug/comments/:id` - Delete comment
- `GET /api/tags` - Get tags

### GraphQL API

Access the GraphQL playground at http://localhost:8080/graphql

Example queries and mutations are available in the GraphQL schema at `app/api/graphql/schema.graphqls`.

## Configuration

Configuration is managed through environment variables or the `app/config.py` file:

- `DATABASE_URL`: Database connection string (default: `sqlite:///./dev.db`)
- `JWT_SECRET`: Secret key for JWT signing
- `JWT_SESSION_TIME`: JWT token expiration time in seconds (default: 86400)
- `DEFAULT_IMAGE`: Default user profile image URL

## Project Structure

```
python/
├── app/
│   ├── api/
│   │   ├── rest/           # FastAPI REST endpoints
│   │   ├── graphql/        # Ariadne GraphQL resolvers
│   │   └── dependencies.py # Dependency injection
│   ├── application/
│   │   ├── services/       # Application services
│   │   └── dto/            # Pydantic DTOs
│   ├── core/
│   │   ├── domain/         # Domain models
│   │   └── repositories/   # Repository interfaces
│   ├── infrastructure/
│   │   ├── db/             # SQLAlchemy models and session
│   │   ├── repositories/   # Repository implementations
│   │   └── security/       # JWT and password hashing
│   ├── config.py           # Configuration
│   └── main.py             # FastAPI application
├── tests/
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── api/                # API tests
├── requirements.txt
├── init_db.py
└── README.md
```

## Comparison with Java Implementation

This Python implementation maintains feature parity with the original Spring Boot application:

| Feature | Java (Spring Boot) | Python (FastAPI) |
|---------|-------------------|------------------|
| REST API | Spring MVC | FastAPI |
| GraphQL | Netflix DGS | Ariadne |
| ORM | MyBatis | SQLAlchemy |
| JWT | jjwt | PyJWT |
| Password Hashing | BCrypt | passlib[bcrypt] |
| Validation | Bean Validation | Pydantic |
| Testing | JUnit | pytest |
| Architecture | DDD + CQRS | DDD + CQRS |

## License

Same as the original Spring Boot implementation.
