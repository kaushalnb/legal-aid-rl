import os
from fastapi import FastAPI, Request
import uvicorn
from env.legal_env import LegalEnv
from env.models import Action

app = FastAPI()

# ✅ Global env instance
env = LegalEnv(difficulty="easy")

# ✅ Shared reset handler
async def handle_reset(request: Request):
    try:
        data = await request.json()
    except:
        data = {}

    difficulty = data.get("difficulty", "easy")

    global env
    env = LegalEnv(difficulty=difficulty)
    obs = env.reset()

    return {
    "status": "ok",
    "observation": obs.model_dump(),  # ✅ not obs.dict()
    "reward": 0.0,
    "done": False,
    "info": {}
}

# ✅ Reset routes
@app.post("/")
async def root_reset(request: Request):
    return await handle_reset(request)

@app.post("/reset")
async def reset1(request: Request):
    return await handle_reset(request)

@app.post("/openenv/reset")
async def openenv_reset(request: Request):
    return await handle_reset(request)

# ✅ Step route — matches your exact Action model fields
@app.post("/openenv/step")
async def openenv_step(request: Request):
    try:
        data = await request.json()
    except:
        data = {}

    action_type = data.get("action_type", "ask_question")
    content = data.get("content", "")

    action = Action(action_type=action_type, content=content)
    result = env.step(action)

    return {
    "observation": result.observation.model_dump(),  # ✅ not .dict()
    "reward": result.reward,
    "done": result.done,
    "info": result.info
}

# ✅ Health check
@app.get("/openenv/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)