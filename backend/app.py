from fastapi import FastAPI
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/chat")
def chat(message: str):

    odgovor = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ti si AeroClub AI asistent za pilotsku obuku."},
            {"role": "user", "content": message}
        ]
    )

    return {"odgovor": odgovor.choices[0].message.content}