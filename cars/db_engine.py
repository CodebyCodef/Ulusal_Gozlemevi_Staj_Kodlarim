from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from db_model import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./cars/cars.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from db_model import Cars
    Base.metadata.create_all(bind=engine)