from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variables for PostgreSQL
DATABASE_URL = os.getenv("NEON_DATABASE_URL", "")

if not DATABASE_URL:
    # If no NEON_DATABASE_URL is provided, fall back to a default format
    # This should be set in the .env file with your Neon PostgreSQL connection string
    raise ValueError("NEON_DATABASE_URL environment variable is required for PostgreSQL")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    """
    Generator function that yields a database session.
    This is used for dependency injection in FastAPI endpoints.
    """
    with Session(engine) as session:
        yield session