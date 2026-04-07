from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/openenv/reset")
def reset():
    return {"status": "reset successful"}

@app.get("/openenv/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)