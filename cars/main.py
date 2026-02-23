from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from db_engine import SessionLocal, init_db
from db_model import Cars

app = FastAPI()

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class CarCreate(BaseModel):

    model: str
    year: int

class Car(CarCreate):
    id: int

    class Config:
        orm_mode = True


@app.post("/car", response_model=Car)
def create_car(car:CarCreate, db: Session = Depends(get_db)):
    db_car = Cars(model=car.model, year=car.year)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

@app.get("/car", response_model=List[Car])
def list_cars(db: Session = Depends(get_db)):
    return db.query(Cars).all()