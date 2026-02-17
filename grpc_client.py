import grpc
import urun_pb2
import urun_pb2_grpc

def run():
    print("🔌 Sunucuya bağlanılıyor...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = urun_pb2_grpc.UrunServisiStub(channel)
        
        # Test 1: Ekleme
        print("--- 1. Ürün Ekleniyor ---")
        yeni_urun = urun_pb2.UrunEkleIstegi(
            ad="Mekanik Klavye",
            fiyat=2500.0,
            stokta_mi=True
        )
        cevap = stub.UrunEkle(yeni_urun)
        print(f"Sonuç: {cevap.mesaj} (ID: {cevap.id})")

        # Test 2: Listeleme
        print("\n--- 2. Liste İsteniyor ---")
        bos = urun_pb2.BosIstek()
        liste = stub.UrunleriListele(bos)
        for urun in liste.urunler:
            print(f"📦 {urun.ad} - {urun.fiyat} TL")

if __name__ == '__main__':
    run()