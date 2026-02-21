from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import sqlite3
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# =========================

# LOAD ENV (lokalno + Render)

# =========================

BASE_DIR = Path(**file**).resolve().parent
ENV_PATH = BASE_DIR.parent / ".env"

load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("OPENAI_API_KEY")

print("OPENAI KEY LOADED:", "YES" if api_key else "NO")

client = OpenAI(api_key=api_key)

app = FastAPI()

# =========================

# DATABASE

# =========================

DB_PATH = BASE_DIR.parent / "database" / "chat.db"

# =========================

# HOME

# =========================

@app.get("/")
def home():
return {"status": "AeroClub AI ONLINE"}

# =========================

# CHAT (NOVI RESPONSES API)

# =========================

@app.get("/chat")
def chat(message: str):

```
try:

    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"Ti si AeroClub AI asistent za pilotsku obuku. Odgovaraj na srpskom.\nKorisnik: {message}"
    )

    ai_text = response.output_text

except Exception as e:

    print("AI ERROR:", str(e))

    ai_text = f"AeroClub AI (fallback mode): Trenutno koristim test režim. Pitanje: {message}"


# SAVE TO DATABASE

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO messages (user_message, ai_response) VALUES (?, ?)",
    (message, ai_text)
)

conn.commit()
conn.close()


return {"odgovor": ai_text}
```

# =========================

# ADMIN API

# =========================

@app.get("/admin")
def admin():

```
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
```

# =========================

# ADMIN PANEL PAGE

# =========================

@app.get("/admin-panel")
def admin_panel():

```
ADMIN_PATH = BASE_DIR.parent / "admin" / "index.html"

return FileResponse(str(ADMIN_PATH))
```
