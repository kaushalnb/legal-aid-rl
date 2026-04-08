import os
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

async def handle_reset(request: Request):
    try:
        data = await request.json()
    except:
        data = {}

    print("START: Reset called")
    print("STEP: Processing request")
    print("END: Done")

    return {"status": "ok"}

# 🔥 SUPPORT ALL ROUTES
@app.post("/")
async def root_reset(request: Request):
    return await handle_reset(request)

@app.post("/reset")
async def reset1(request: Request):
    return await handle_reset(request)

@app.post("/openenv/reset")
async def reset2(request: Request):
    return await handle_reset(request)

@app.get("/openenv/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)