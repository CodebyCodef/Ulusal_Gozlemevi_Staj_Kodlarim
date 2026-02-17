from sqlalchemy import Column, Integer, String, Boolean, Float
import databaseEngine as engine # Motor dosyasından Base sınıfını alıyoruz

class Urun(engine.Base):
    __tablename__ = "urunler"

    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, index=True)
    fiyat = Column(Float)
    stokta_mi = Column(Boolean, default=True) # DİKKAT: İsmi 'stokta_mi'