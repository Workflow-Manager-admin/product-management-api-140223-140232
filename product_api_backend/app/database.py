from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.models.product import Base
import os

# PUBLIC_INTERFACE
def get_db_url():
    """
    Retrieves SQLite database URL from environment variable.
    """
    db_path = os.getenv("SQLITE_DB", "sqlite:///products.db")
    if db_path.startswith("sqlite:///"):
        return db_path
    return f"sqlite:///{db_path}"

engine = create_engine(get_db_url(), connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# PUBLIC_INTERFACE
def init_db():
    """
    Initializes the product database and creates tables if they don't exist.
    """
    Base.metadata.create_all(bind=engine)
