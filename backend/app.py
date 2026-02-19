from fastapi import FastAPI
import os
from openai import OpenAI

app = FastAPI()

import os
from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY")

print("API KEY LOADED:", api_key[:10] if api_key else "NONE")

client = OpenAI(api_key=api_key)

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