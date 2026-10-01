import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# For now, we'll default to a local SQLite database file named 'portal.db'
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./portal.db")

# 1. Create the SQLAlchemy engine (manages connection pools)
# check_same_thread is only needed for SQLite to allow multiple threads
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# 2. Create a session factory to handle individual database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create a base class for all our database models to inherit from
class Base(DeclarativeBase):
    pass

# 4. Dependency function to get a database session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()