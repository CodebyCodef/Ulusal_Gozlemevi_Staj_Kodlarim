from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dataModel import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./deneme.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)   
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from dataModel import Person
    from dataModel import Parents
    Base.metadata.create_all(bind=engine)