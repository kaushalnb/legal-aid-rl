from fastapi import FastAPI

app = FastAPI()

@app.post("/reset")
def reset():
    return {"status": "reset successful"}

@app.get("/")
def home():
    return {"message": "API running"}