from sqlalchemy import Column, Integer, String, Boolean, Float, VARCHAR, DateTime
from db_Engine import Base
from datetime import datetime

class Personel(Base):
    __tablename__ = "personeller"

    sicil_no = Column(Integer, primary_key=True, index=True)
    ad = Column(String, index=True)
    soyad = Column(String, index=True)
    foto_url = Column(String, nullable=True)

