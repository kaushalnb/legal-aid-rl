import os
from fastapi import FastAPI, Request
import uvicorn
from env.legal_env import LegalEnv
from env.models import Action

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

app = FastAPI()
env = LegalEnv(difficulty="easy")

async def handle_reset(request: Request):
    try:
        data = await request.json()
    except:
        data = {}

    difficulty = data.get("difficulty", "easy")
    global env
    env = LegalEnv(difficulty=difficulty)
    obs = env.reset()

    print("[START] task=legal-aid env=legal-aid-rl model=" + MODEL_NAME, flush=True)
    print("[STEP] step=0 action=reset reward=0.00 done=false error=null", flush=True)

    return {
        "status": "ok",
        "observation": obs.model_dump(),
        "reward": 0.0,
        "done": False,
        "info": {}
    }

@app.post("/")
async def root_reset(request: Request):
    return await handle_reset(request)

@app.post("/reset")
async def reset1(request: Request):
    return await handle_reset(request)

@app.post("/openenv/reset")
async def openenv_reset(request: Request):
    return await handle_reset(request)

@app.post("/openenv/step")
async def openenv_step(request: Request):
    try:
        data = await request.json()
    except:
        data = {}

    action = Action(
        action_type=data.get("action_type", "ask_question"),
        content=data.get("content", "")
    )
    result = env.step(action)

    print(f"[STEP] step=1 action={action.content[:30]} reward={result.reward:.2f} done={str(result.done).lower()} error=null", flush=True)

    return {
        "observation": result.observation.model_dump(),
        "reward": result.reward,
        "done": result.done,
        "info": result.info
    }

@app.get("/openenv/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)