from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Kullanıcıları RAM belleğinde tutacak liste
users = []

# Pydantic modeli - gelen veriyi kontrol etmek için
class User(BaseModel):
    name: str
    email: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/users")
def get_users():
    """Tüm kullanıcıları listele"""
    return {"users": users}

@app.post("/api/user")
def create_user(user: User):
    """Yeni kullanıcı ekle"""
    user_data = user.dict()
    user_data["id"] = len(users) + 1  # ID otomatik oluştur
    users.append(user_data)
    return {"message": "User created successfully", "user": user_data}