from sqlmodel import create_engine, Session
from config.settings import settings
import os


# Create the database engine
# Use neon database if available, otherwise use default database
DATABASE_URL = settings.neon_database_url or settings.database_url

# Create the database engine with appropriate settings for different databases
if DATABASE_URL.startswith("sqlite"):
    # For SQLite, don't use connection pooling
    engine = create_engine(DATABASE_URL)
else:
    # For PostgreSQL, use appropriate connection settings
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def get_session():
    """Generator function that yields a database session."""
    with Session(engine) as session:
        yield session