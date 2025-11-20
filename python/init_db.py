from app.infrastructure.db.models import Base
from app.infrastructure.db.session import engine

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
