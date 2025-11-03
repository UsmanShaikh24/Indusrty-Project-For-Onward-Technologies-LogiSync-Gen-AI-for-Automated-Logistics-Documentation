from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.database import Base
from src.config import settings

# Create database URL
DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"

# Create database engine
engine = create_engine(DATABASE_URL)

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create SessionLocal class for database sessions
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
