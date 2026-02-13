from fastapi import FastAPI

app = FastAPI()


# mesaj = {"mesaj": "Merhaba Dünya!"}
# @app.get("/")
# def cache():
#     return mesaj  


mesajlar = []

@app.post("/api/gonder")
def gonder(mesaj: str):
    mesajlar.append(mesaj)
    return {"message": "Mesaj başarıyla gönderildi", "mesaj": mesaj}


@app.get("/api/mesajlar")
def mesajlarim():
    return {"mesajlar": mesajlar}


@app.delete("/api/mesajlar")
def mesajlari_sil():
    mesajlar.clear()
    return {"message": "Tüm mesajlar silindi"}