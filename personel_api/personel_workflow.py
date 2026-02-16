import os
from dotenv import load_dotenv

# .env dosyasını en başta yükle (imports'ten önce!)
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from typing import List
from pydantic import BaseModel

import personel_db as models
import db_Engine as engine

# DEBUG: Hangi veritabanına bağlandığını kontrol et
print(f"DEBUG: DATABASE_URL = {os.getenv('DATABASE_URL', 'NOT SET')}")
print(f"DEBUG: Kullanılan bağlantı: {engine.SQLALCHEMY_DATABASE_URL}")

models.Base.metadata.create_all(bind=engine.engine)

personel_app = FastAPI(
    title="Personel Yönetim API",
    description="Personel bilgilerini yönetmek için REST API",
    version="1.0.0"
)

# CORS Middleware - Frontend'den çağrıları kabul etmek için
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

personel_app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = engine.SessionLocal()
    try:
        yield db
    finally:
        db.close()  

class PersonelBase(BaseModel):
    sicil_no: int
    ad: str
    soyad: str

class PersonelCreate(PersonelBase):
    pass

class Personel(PersonelBase):
    class Config:
        orm_mode = True

@personel_app.post("/api/personeller", response_model=Personel)
def personel_ekle(personel: PersonelCreate, db: Session = Depends(get_db)):
    db_personel = models.Personel(sicil_no=personel.sicil_no, ad=personel.ad, soyad=personel.soyad)
    db.add(db_personel)
    db.commit()
    db.refresh(db_personel)
    return db_personel

@personel_app.get("/api/personeller", response_model=List[Personel])
def personel_listesi(db: Session = Depends(get_db)):
    return db.query(models.Personel).all()


@personel_app.get("/api/personeller/{sicil_no}", response_model=Personel)
def personel_getir(sicil_no: int, db: Session = Depends(get_db)):
    db_personel = db.query(models.Personel).filter(models.Personel.sicil_no == sicil_no).first()
    if db_personel is None:
        raise HTTPException(status_code=404, detail="Personel bulunamadı")
    return db_personel


@personel_app.put("/api/personeller/{sicil_no}", response_model=Personel)
def personel_guncelle(sicil_no: int, personel: PersonelCreate, db: Session = Depends(get_db)):
    db_personel = db.query(models.Personel).filter(models.Personel.sicil_no == sicil_no).first()
    if db_personel is None:
        raise HTTPException(status_code=404, detail="Personel bulunamadı")
    db_personel.ad = personel.ad
    db_personel.soyad = personel.soyad
    db.commit()
    db.refresh(db_personel)
    return db_personel

@personel_app.delete("/api/personeller/{sicil_no}")
def personel_sil(sicil_no: int, db: Session = Depends(get_db)):
    db_personel = db.query(models.Personel).filter(models.Personel.sicil_no == sicil_no).first()
    if db_personel is None:
        raise HTTPException(status_code=404, detail="Personel bulunamadı")
    db.delete(db_personel)
    db.commit()
    return {"detail": "Personel silindi"}