import speech_recognition as sr
import requests
import asyncio
import edge_tts
import os

# 🔑 API KEY
OPENROUTER_API_KEY = "sk-or-v1-7ebf26dcc25c520681350eb7747c9686026a98428b94b8b93ad21266c718850cI_KEY"

# 🎤 Dinleme
def dinle():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Dinleniyor...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except:
            return "Anlayamadım"

    try:
        text = r.recognize_google(audio, language="tr-TR")
        print("Sen:", text)
        return text
    except:
        return "Anlayamadım"

# 🤖 AI Cevap
def ai_cevap(soru):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Komik AI"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "Sen aşırı komik, esprili, hafif dalga geçen Türkçe konuşan bir asistansın. Kısa ve eğlenceli cevap ver."
            },
            {
                "role": "user",
                "content": soru
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        result = response.json()

        print("DEBUG:", result)

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return "API hata verdi 😅"

    except Exception as e:
        print("Hata:", e)
        return "Sistem çöktü ama ben hâlâ karizmatiğim 😎"

# 🔊 Türkçe doğal ses (Edge TTS)
async def konus_async(metin):
    tts = edge_tts.Communicate(metin, voice="tr-TR-AhmetNeural")
    await tts.save("cevap.mp3")
    os.system("start cevap.mp3")

def konus(metin):
    asyncio.run(konus_async(metin))

# 🔁 Sürekli konuşma (Jarvis modu)
def surekli_konus():
    print("Sistem hazır. Konuşmaya başlayabilirsin...\n")

    while True:
        kullanici = dinle()

        if kullanici == "Anlayamadım":
            konus("Seni anlayamadım, tekrar dener misin?")
            continue

        cevap = ai_cevap(kullanici)

        print("AI:", cevap)
        konus(cevap)

# 🚀 Başlat
if __name__ == "__main__":
    surekli_konus()