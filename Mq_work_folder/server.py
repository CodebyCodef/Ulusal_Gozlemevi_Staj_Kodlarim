import zmq
import time

# ZeroMQ ortamını hazırlıyoruz
context = zmq.Context()
socket = context.socket(zmq.REP) # REP (Reply/Yanıt) soketi
socket.bind("tcp://*:5555") # 5555 portunu dinlemeye başlıyoruz

print("Yapay Zeka Öneri Motoru başlatıldı. İstekler bekleniyor...")

while True:
    # İstemciden gelen mesajı alıyoruz
    mesaj = socket.recv_string()
    print(f"[Sunucu] Gelen veri: {mesaj}")

    # Sanki derin öğrenme modeli çalışıyormuş gibi 1 saniye bekletelim
    time.sleep(1)

    # Gelen veriye göre basit bir mantıkla yanıt dönelim
    if "Spor" in mesaj:
        yanit = "Öneri: Beyaz sneaker ve gri eşofman altı"
    elif "Klasik" in mesaj:
        yanit = "Öneri: Siyah kumaş pantolon ve beyaz gömlek"
    else:
        yanit = "Öneri: Standart kot pantolon ve tişört"

    # Yanıtı istemciye geri gönderiyoruz
    socket.send_string(yanit)