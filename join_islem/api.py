from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from engine import SessionLocal, init_db
from model import Market, Reyon

app = FastAPI()

init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class productCreate(BaseModel):
    name: str
    price: float
    reyon_id: int
   

class product(productCreate):
    
    id: int
    reyon_id: int

    class config:
        orm_mode = True


class reyonCreate(BaseModel):
    reyon_name: str

class reyon(reyonCreate):
    id: int 

    class config:
        orm_mode = True



@app.post("/reyon", response_model=reyon)
def create_reyon(p: reyonCreate, db: Session = Depends(get_db)):
    obj = Reyon(reyon_name=p.reyon_name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/reyon")
def list_reyon(db: Session = Depends(get_db)):
    reyonlar = db.query(Reyon).all()

    for r in reyonlar:
        print(r.reyon_name)

    return reyonlar



@app.post("/product", response_model=product)
def create_product(p: productCreate, db: Session = Depends(get_db)):
    reyon = db.query(Reyon).filter(Reyon.id == p.reyon_id).first()
    if not reyon:
        raise HTTPException(status_code=404, detail="Reyon not found")
    obj = Market(name=p.name, price=p.price, reyon_id=p.reyon_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj




@app.get("/product")
def list_product(db: Session = Depends(get_db)):
    
    products = db.query(Market).all()

    for p in products:
        print(p.name, p.price, p.reyon.reyon_name)

    return products