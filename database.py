from sqlalchemy import Column, Integer, String, Boolean, Float
from databaseEngine import Base


class Urun(Base):
    __tablename__ = "urunler"

    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, index=True)
    fiyat = Column(Float)
    stokta = Column(Boolean, default=True)

