import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker

# PostgreSQL bağlantı URL'sini env değişkeninden oku
# Fallback: SQLite (eğer env set edilmemişse yerel test için)
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./sql_app.db"
)

# PostgreSQL ise SQLite-özel connect_args kullanma
if SQLALCHEMY_DATABASE_URL.startswith("postgresql"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    # SQLite için eski ayar
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()