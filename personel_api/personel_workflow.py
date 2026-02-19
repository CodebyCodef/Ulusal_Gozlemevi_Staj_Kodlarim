import os
from dotenv import load_dotenv

# .env dosyasını en başta yükle (imports'ten önce!)
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from typing import List
from typing import Optional
from pydantic import BaseModel

from fastapi import File, UploadFile
import httpx
import shutil
from datetime import datetime
import traceback


import personel_db as models
import db_Engine as engine

 

# DEBUG: Hangi veritabanına bağlandığını kontrol et
print(f"DEBUG: DATABASE_URL = {os.getenv('DATABASE_URL', 'NOT SET')}")
print(f"DEBUG: Kullanılan bağlantı: {engine.SQLALCHEMY_DATABASE_URL}")

models.Base.metadata.create_all(bind=engine.engine)

personel_app = FastAPI(
    title="Personel Yönetim API",
    description="Personel bilgi yönetimi",
    version="0.0.1"
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
    foto_url: Optional[str] = None
    

class PersonelCreate(PersonelBase):
    pass

class Personel(PersonelBase):
    class Config:
        orm_mode = True


MAX_BYTES = 5 * 1024 * 1024  # 5MB


@personel_app.post("/api/personeller")
async def personel_ekle(
    sicil_no: int = Form(...),
    ad: str = Form(...),
    soyad: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        # Sicil no kontrolü
        if db.query(models.Personel).filter(models.Personel.sicil_no == sicil_no).first():
            raise HTTPException(status_code=400, detail="Bu sicil numarası zaten kayıtlı")
        
        foto_url = None

        # Eğer fotoğraf gönderildiyse → External API'ye ilet
        if file and file.filename:
            print(f"DEBUG: Fotoğraf alındı - filename: {file.filename}, content_type: {file.content_type}")
            
            # Dosya tipi kontrolü
            if not file.content_type:
                raise HTTPException(status_code=400, detail="Content-Type bilgisi yok")
            
            allowed = {"image/jpeg", "image/png", "image/jpg"}
            if file.content_type not in allowed:
                raise HTTPException(status_code=400, detail="Desteklenmeyen dosya türü")
            
            file_bytes = await file.read()
            print(f"DEBUG: Dosya boyutu: {len(file_bytes)} bytes")
            
            if len(file_bytes) > MAX_BYTES:
                raise HTTPException(status_code=400, detail="Dosya çok büyük")
            
            external_url = os.getenv("EXTARNAL_API_URL")
            print(f"DEBUG: External URL: {external_url}")
            
            if not external_url:
                raise HTTPException(
                    status_code=500,
                    detail="EXTARNAL_API_URL ortam değişkeni tanımlı değil."
                )
            
            files_payload = {
                "file": (file.filename, file_bytes, file.content_type)
            }
            data_payload = {"sicil_no": str(sicil_no)}

            timeout = httpx.Timeout(30.0, connect=10.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                try:
                    resp = await client.post(
                        external_url,
                        files=files_payload,
                        data=data_payload
                    )
                    print(f"DEBUG: External API status: {resp.status_code}")
                    print(f"DEBUG: External API response: {resp.text[:500]}")
                    resp.raise_for_status()
                except httpx.RequestError as exc:
                    print(f"HATA: External API bağlantı hatası: {exc}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Fotoğraf yükleme başarısız: {exc}"
                    )
                except httpx.HTTPStatusError as exc:
                    print(f"HATA: External API HTTP hatası: {resp.status_code} - {resp.text[:500]}")
                    raise HTTPException(
                        status_code=resp.status_code,
                        detail=f"External API hata döndü: {resp.text}"
                    )

            try:
                result = resp.json()
                print(f"DEBUG: External API JSON yanıtı: {result}")
            except Exception:
                result = {"response_text": resp.text}
                print(f"DEBUG: External API text yanıtı: {resp.text[:500]}")

            # External API'den dönen dosya yolunu al
            foto_url = result.get("foto_url") or result.get("url") or result.get("file_url") or result.get("file_path") or result.get("path")
            print(f"DEBUG: Bulunan foto_url: {foto_url}")
        else:
            print(f"DEBUG: Fotoğraf gönderilmedi. file={file}, filename={file.filename if file else 'None'}")

        # Personeli veritabanına kaydet
        db_personel = models.Personel(
            sicil_no=sicil_no, 
            ad=ad, 
            soyad=soyad,
            foto_url=foto_url
        )
        db.add(db_personel)
        db.commit()
        db.refresh(db_personel)
        
        print(f"DEBUG: Personel kaydedildi - sicil: {sicil_no}, ad: {ad}, foto_url: {foto_url}")
        
        return {
            "sicil_no": db_personel.sicil_no,
            "ad": db_personel.ad,
            "soyad": db_personel.soyad,
            "foto_url": db_personel.foto_url
        }
    
    except HTTPException:
        raise  # HTTPException'ları olduğu gibi gönder
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"HATA YAKALANDI: {type(e).__name__}: {e}")
        traceback.print_exc()
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=f"Sunucu hatası: {str(e)}")


# ---------------------------------------------------------------------------------------------------------
# FOTOĞRAF PROXY - Frontend fotoğrafları bu endpoint üzerinden çeker
# ---------------------------------------------------------------------------------------------------------

@personel_app.get("/api/personeller/foto/{sicil_no}")
async def personel_foto_proxy(sicil_no: int, db: Session = Depends(get_db)):
    """
    Personelin fotoğrafını External API'den çekip frontend'e döner.
    Frontend doğrudan External API'ye erişemiyorsa bu proxy kullanılır.
    """
    from starlette.responses import StreamingResponse
    import io
    
    db_personel = db.query(models.Personel).filter(models.Personel.sicil_no == sicil_no).first()
    if db_personel is None:
        raise HTTPException(status_code=404, detail="Personel bulunamadı")
    
    if not db_personel.foto_url:
        raise HTTPException(status_code=404, detail="Bu personel için fotoğraf yok")
    
    # External API'den fotoğrafı çek
    timeout = httpx.Timeout(10.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            resp = await client.get(db_personel.foto_url)
            resp.raise_for_status()
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Fotoğraf alınamadı: {exc}")
    
    # Content-Type'ı belirle
    content_type = resp.headers.get("content-type", "image/jpeg")
    
    return StreamingResponse(
        io.BytesIO(resp.content),
        media_type=content_type
    )


@personel_app.get("/api/personeller", response_model=List[Personel])
def personel_listesi(db: Session = Depends(get_db)):
    return db.query(models.Personel).all()


@personel_app.get("/api/personeller/{sicil_no}", response_model=Personel)
def personel_getir(sicil_no: int, db: Session = Depends(get_db)):
    db_personel = db.query(models.Personel).filter(models.Personel.sicil_no == sicil_no).first()
    if db_personel is None:
        raise HTTPException(status_code=404, detail="Personel bulunamadı")
    return db_personel


@personel_app.put("/api/personeller/{sicil_no}")
async def personel_guncelle(
    sicil_no: int,
    ad: str = Form(...),
    soyad: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    db_personel = db.query(models.Personel).filter(models.Personel.sicil_no == sicil_no).first()
    if db_personel is None:
        raise HTTPException(status_code=404, detail="Personel bulunamadı")
    
    # Ad ve soyad güncelle
    db_personel.ad = ad
    db_personel.soyad = soyad

    # Eğer yeni fotoğraf gönderildiyse → External API'ye ilet
    if file and file.filename:
        allowed = {"image/jpeg", "image/png", "image/jpg"}
        if file.content_type not in allowed:
            raise HTTPException(status_code=400, detail="Desteklenmeyen dosya türü")
        
        file_bytes = await file.read()
        if len(file_bytes) > MAX_BYTES:
            raise HTTPException(status_code=400, detail="Dosya çok büyük")
        
        external_url = os.getenv("EXTARNAL_API_URL")
        if not external_url:
            raise HTTPException(status_code=500, detail="EXTARNAL_API_URL tanımlı değil")
        
        files_payload = {"file": (file.filename, file_bytes, file.content_type)}
        data_payload = {"sicil_no": str(sicil_no)}
        timeout = httpx.Timeout(30.0, connect=10.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                resp = await client.post(external_url, files=files_payload, data=data_payload)
                resp.raise_for_status()
            except httpx.RequestError as exc:
                raise HTTPException(status_code=500, detail=f"Fotoğraf yükleme başarısız: {exc}")
            except httpx.HTTPStatusError as exc:
                raise HTTPException(status_code=resp.status_code, detail=f"External API hata döndü: {resp.text}")

        try:
            result = resp.json()
        except Exception:
            result = {}

        foto_url = result.get("foto_url") or result.get("url") or result.get("file_url") or result.get("file_path") or result.get("path")
        if foto_url:
            db_personel.foto_url = foto_url

    db.commit()
    db.refresh(db_personel)
    
    return {
        "sicil_no": db_personel.sicil_no,
        "ad": db_personel.ad,
        "soyad": db_personel.soyad,
        "foto_url": db_personel.foto_url
    }

@personel_app.delete("/api/personeller/{sicil_no}")
def personel_sil(sicil_no: int, db: Session = Depends(get_db)):
    db_personel = db.query(models.Personel).filter(models.Personel.sicil_no == sicil_no).first()
    if db_personel is None:
        raise HTTPException(status_code=404, detail="Personel bulunamadı")
    db.delete(db_personel)
    db.commit()
    return {"detail": "Personel silindi"}



