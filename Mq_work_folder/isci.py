import zmq
import time
import random

context = zmq.Context()
# Görevleri çekeceğimiz için PULL soketi kullanıyoruz
socket = context.socket(zmq.PULL)
socket.connect("tcp://localhost:5557")

print("İndirme İşçisi (Worker) hazır. Görevler bekleniyor...")

while True:
    # Kuyruktan sıradaki dosyayı çekiyoruz
    dosya = socket.recv_string()
    print(f"[-] Görev Alındı: {dosya} indiriliyor...")
    
    # Dosya boyutuna göre indirme süresinin değiştiğini simüle edelim (1 ile 4 sn arası)
    islem_suresi = random.randint(1, 4)
    time.sleep(islem_suresi) 
    
    print(f"[+] Tamamlandı: {dosya} başarıyla indirildi! (Süre: {islem_suresi}sn)\n")