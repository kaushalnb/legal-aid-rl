from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/openenv/reset")
async def reset(request: Request):
    data = await request.json()
    return {"status": "ok"}

@app.get("/openenv/health")
def health():
    return {"status": "ok"}