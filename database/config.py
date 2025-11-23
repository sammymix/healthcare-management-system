import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "postgresql://admin:password@localhost:5432/healthcare_db"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # Set to False in production - shows SQL queries
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Database dependency for FastAPI
    Usage: 
        db: Session = Depends(get_db)
    """
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

def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            print("✅ Database connection: SUCCESS")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
