import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL from settings
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "The DATABASE_URL environement variable is not defined."
        "Please check your settings and .env file."
        )

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Generator to get a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
