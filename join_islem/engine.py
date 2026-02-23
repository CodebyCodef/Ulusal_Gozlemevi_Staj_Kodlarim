from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from model import Base


DATABASE_URL = "sqlite:///./products.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Import models here to ensure they are registered with Base.metadata
    from model import Market  
    from model import Reyon # noqa: F401
    Base.metadata.create_all(bind=engine)