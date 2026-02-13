from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

import database as models
import databaseEngine as engine

models.Base.metadata.create_all(bind=engine.engine)


app = FastAPI()

def get_db():
    db = engine.SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UrunBase(BaseModel):
    id: int
    ad: str 
    fiyat: float
    stok: bool = True

# Buradaki "pass" ifadesi, UrunCreate sınıfının UrunBase sınıfından türetildiğini ve
#  şu anda ek bir özellik veya davranış içermediğini belirtir. 
# Bu, gelecekte UrunCreate sınıfına 
# özel özellikler eklemek istediğinizde kolayca genişletilebilir hale getirir.

#kısaca inheritance diyebiliriz.
class UrunCreate(UrunBase):
    pass



class Urun(UrunBase):
    id:int 
    class Config:
        orm_mode = True


@app.post("/api/urunler", response_model=Urun)
def urun_ekle(urun: UrunCreate, db: Session = Depends(get_db)):
    db_urun = models.Urun(ad=urun.ad, fiyat=urun.fiyat, stokta=urun.stok)
    db.add(db_urun)
    db.commit()
    db.refresh(db_urun)
    return db_urun
   
@app.get("/api/urunler/", response_model=List[Urun])
def urunleri_listele(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    urunler = db.query(models.Urun).offset(skip).limit(limit).all()
    return urunler

@app.get("/api/urunler/{urun_id}", response_model=Urun)
def urun_getir(urun_id : int, db: Session = Depends(get_db)):
    db_urun = db.query(models.Urun).filter(models.Urun.id == urun_id).first()
    if db_urun is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return db_urun




