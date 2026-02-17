import grpc
from concurrent import futures
import time

import urun_pb2
import urun_pb2_grpc

import database as models
import databaseEngine as engine

class UrunServisi(urun_pb2_grpc.UrunServisiServicer):
    def UrunEkle(self, request, context):
        print(f"📥 Yeni ürün isteği: {request.ad}")
        db = engine.SessionLocal()

        try:
            yeni_urun = models.Urun(
                ad=request.ad,
                fiyat=request.fiyat,
                stokta_mi=request.stokta_mi
            )
            db.add(yeni_urun)
            db.commit()
            db.refresh(yeni_urun)

            return urun_pb2.UrunYaniti(
                id=yeni_urun.id,
                ad=yeni_urun.ad,
                fiyat=yeni_urun.fiyat,
                stokta_mi=yeni_urun.stokta_mi,
                mesaj="Ürün başarıyla eklendi!"
            )
        except Exception as e:
            print(f"Hata: {e}")
            return urun_pb2.UrunYaniti(mesaj="Hata oluştu")
        finally:
            db.close()

    def UrunleriListele(self, request, context):
        print("📋 Ürün listesi istendi...")
        db = engine.SessionLocal()
        try:
            db_urunler = db.query(models.Urun).all()
            liste_yaniti = urun_pb2.UrunListesiYaniti()
            
            for ur in db_urunler:
                grpc_urun = urun_pb2.UrunYaniti(
                    id=ur.id,
                    ad=ur.ad,
                    fiyat=ur.fiyat,
                    stokta_mi=ur.stokta_mi
                )
                liste_yaniti.urunler.append(grpc_urun)
                
            return liste_yaniti
        finally:
            db.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    urun_pb2_grpc.add_UrunServisiServicer_to_server(UrunServisi(), server)
    server.add_insecure_port('[::]:50051')
    print("🚀 gRPC Sunucusu 50051 portunda çalışıyor...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()