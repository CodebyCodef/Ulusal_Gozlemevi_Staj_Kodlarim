from sqlalchemy import ForeignKey, String, Integer, Column
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)

    parents = relationship("Parents", back_populates="person")



class Parents(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    
    person_id = Column(Integer, ForeignKey("person.id"))
    person = relationship("Person", back_populates="parents") 