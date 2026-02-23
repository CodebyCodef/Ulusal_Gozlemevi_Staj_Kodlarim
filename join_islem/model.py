from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Reyon(Base):
    __tablename__ = "reyon"

    id = Column(Integer, primary_key=True)
    reyon_name = Column(String)
    
    products = relationship("Market", back_populates="reyon")


class Market(Base):
    __tablename__ = "market"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    reyon_id = Column(Integer, ForeignKey("reyon.id"))
    reyon = relationship("Reyon", back_populates="products")