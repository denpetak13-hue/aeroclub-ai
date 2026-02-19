from fastapi import FastAPI
import os
from openai import OpenAI

app = FastAPI()

# učitaj API ključ
api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


@app.get("/chat")
def chat(message: str):

    try:

        odgovor = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ti si AeroClub AI asistent za pilotsku obuku."},
                {"role": "user", "content": message}
            ]
        )

        return {"odgovor": odgovor.choices[0].message.content}

    except Exception as e:

        print("AI ERROR:", str(e))

        return {
            "odgovor": f"AeroClub AI (fallback mode): Trenutno koristim test režim. Pitanje: {message}"
        }


@app.get("/admin")
def admin():

    return {"status": "AeroClub AI radi"}