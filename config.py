import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Database configuration - choose one based on your setup

# Option 1: Local Docker setup (use this if running via docker-compose)
DATABASE_URL = "postgresql://admin:password@localhost:5432/healthcare_db"

# Option 2: Direct Docker container access (use within Docker network)
# DATABASE_URL = "postgresql://admin:password@postgres:5432/healthcare_db"

# Option 3: For testing without Docker
# DATABASE_URL = "sqlite:///./test.db"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # Set to False in production
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all tables in the database (for testing)"""
    Base.metadata.drop_all(bind=engine)
