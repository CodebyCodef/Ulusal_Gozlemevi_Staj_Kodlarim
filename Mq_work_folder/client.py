import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ) # REQ (Request/İstek) soketi

# Sunucunun çalıştığı adrese bağlanıyoruz (Kendi bilgisayarımız olduğu için localhost)
print("Öneri motoruna bağlanılıyor...")
socket.connect("tcp://localhost:5555")

# Test için farklı tarzlar gönderiyoruz
tarzlar = ["Müşteri: Erkek, Tarz: Spor", "Müşteri: Erkek, Tarz: Klasik", "Müşteri: Erkek, Tarz: Günlük"]

for istek, tarz in enumerate(tarzlar):
    print(f"\n[İstemci] {istek + 1}. İstek gönderiliyor: {tarz}")
    socket.send_string(tarz)
    
    # Sunucudan gelecek öneriyi bekliyoruz
    gelen_yanit = socket.recv_string()
    print(f"[İstemci] Gelen Yanıt: {gelen_yanit}")