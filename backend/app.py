from fastapi import FastAPI

app = FastAPI()

istorija = []

@app.get("/chat")
def chat(message: str):

    istorija.append(message)

    odgovor = "AeroClub AI: " + message

    return {"odgovor": odgovor}


@app.get("/admin")
def admin():

    return {"poruke": istorija}