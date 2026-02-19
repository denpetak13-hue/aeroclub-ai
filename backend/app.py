from fastapi import FastAPI
import os
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv

# učitaj .env fajl iz root foldera
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")

load_dotenv(dotenv_path=ENV_PATH)

app = FastAPI()

api_key = os.environ.get("OPENAI_API_KEY")



client = OpenAI(api_key=api_key)
# --- Database path ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "chat.db")
from fastapi.responses import FileResponse

@app.get("/admin-panel")
def admin_panel():
    return FileResponse("../admin/index.html")

# --- HOME ---
@app.get("/")
def home():
    return {"status": "AeroClub AI ONLINE"}


# --- CHAT ---
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

        ai_text = odgovor.choices[0].message.content

    except Exception as e:

        print("AI ERROR:", str(e))

        ai_text = f"AeroClub AI (fallback mode): Trenutno koristim test režim. Pitanje: {message}"


    # --- SAVE TO DATABASE ---
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (user_message, ai_response) VALUES (?, ?)",
        (message, ai_text)
    )

    conn.commit()
    conn.close()


    return {"odgovor": ai_text}


# --- ADMIN DASHBOARD API ---
@app.get("/admin")
def admin():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, user_message, ai_response
        FROM messages
        ORDER BY id DESC
        LIMIT 50
    """)

    rows = cursor.fetchall()

    conn.close()

    return {"messages": rows}