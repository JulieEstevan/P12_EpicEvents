import os
import sys

# Ensure the project root is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def initialize_database():
    """Initialize the database by importing all models."""
    
    # Import engine
    from .database import engine
    # Import models to ensure they are registered with SQLAlchemy
    from models.base import Base
    from models.client import Client
    from models.contract import Contract
    from models.event import Event
    from models.user import User

    try:
        # Create all tables in the database
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully.")
    except Exception as e:
        print(f"An error occurred while initializing the database: {e}")

if __name__ == "__main__":
    initialize_database()
