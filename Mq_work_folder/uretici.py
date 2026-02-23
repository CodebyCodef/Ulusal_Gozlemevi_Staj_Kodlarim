import zmq
import time

context = zmq.Context()
# Görevleri dağıtacağımız için PUSH soketi kullanıyoruz
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5557") # 5557 portundan yayın yapacağız

print("Mobil uygulama arka planı çalışıyor. Dosya indirme kuyruğu hazır...")
print("İşçilerin bağlanması için 5 saniye bekleniyor...\n")
time.sleep(5) # Sen diğer terminalleri açana kadar beklemesi için

# Kullanıcıların indirmek istediği dosyalar (Kuyruğa girecek görevler)
dosyalar = ["rapor_2026.pdf", "tatil_fotografi.png", "kurulum_dosyasi.exe", "egitim_videosu.mp4", "veritabani.sql"]

for dosya in dosyalar:
    print(f"[Kuyruğa Eklendi] Görev: {dosya} indirilecek.")
    socket.send_string(dosya)
    time.sleep(0.5) # İsteklerin peş peşe gelmesini simüle ediyoruz