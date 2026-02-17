from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

import database as models        # Tablo dosyamız
import databaseEngine as engine  # Motor dosyamız

# Tabloları oluştur
models.engine.Base.metadata.create_all(bind=engine.engine)

app = FastAPI()

# Veritabanı Oturumu Aç/Kapa
def get_db():
    db = engine.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic Şemaları ---
class UrunBase(BaseModel):
    ad: str
    fiyat: float
    stokta_mi: bool = True

class UrunCreate(UrunBase):
    pass

class Urun(UrunBase):
    id: int
    class Config:
        orm_mode = True

# --- Endpointler ---
@app.post("/urunler/", response_model=Urun)
def urun_ekle(urun: UrunCreate, db: Session = Depends(get_db)):
    db_urun = models.Urun(ad=urun.ad, fiyat=urun.fiyat, stokta_mi=urun.stokta_mi)
    db.add(db_urun)
    db.commit()
    db.refresh(db_urun)
    return db_urun

@app.get("/urunler/", response_model=List[Urun])
def urunleri_listele(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    urunler = db.query(models.Urun).offset(skip).limit(limit).all()
    return urunler