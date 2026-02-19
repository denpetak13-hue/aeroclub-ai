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

        # FREE MODE fallback
        return {"odgovor": f"AeroClub AI (test mode): Primio sam pitanje → {message}"}