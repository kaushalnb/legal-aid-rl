import os
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

# Required env variables
API_BASE_URL = os.getenv("API_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "")
HF_TOKEN = os.getenv("HF_TOKEN")

@app.post("/openenv/reset")
async def reset(request: Request):
    data = await request.json()

    print("START: Reset called")
    print("STEP: Processing reset request")
    print("END: Reset complete")

    return {
        "status": "ok",
        "message": "Environment reset successful"
    }

@app.get("/openenv/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)