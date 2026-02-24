from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List
from sqlalchemy.orm import Session
from dataEngine import SessionLocal, init_db
from dataModel import Parents, Person

app = FastAPI()

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class ParentsCreate(BaseModel):
    name: str
    surname: str
    person_id: int
    

class ParentsRead(ParentsCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PersonCreate(BaseModel):
    name: str
    surname: str


class PersonRead(PersonCreate):
    id: int

    parents: List[ParentsRead] = []

    model_config = ConfigDict(from_attributes=True)




@app.post("/person", response_model=PersonRead)
def create_person(p: PersonCreate, db: Session = Depends(get_db)):
    obj = Person(name=p.name, surname=p.surname)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/person",response_model=List[PersonRead])
def list_person(db: Session = Depends(get_db)):
    people = db.query(Person).all()

  
    return people


@app.post("/parents", response_model=ParentsRead)
def create_parents(p: ParentsCreate, db: Session = Depends(get_db)):
    obj = Parents(name=p.name, surname=p.surname, person_id=p.person_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/parents",response_model=List[ParentsRead])
def list_parents(db: Session = Depends(get_db)):
    parents_list = db.query(Parents).all()
    return parents_list


