import asyncio
import os
import textwrap
from typing import List, Optional
from openai import OpenAI
from env.legal_env import LegalEnv
from env.models import Action

# ✅ Required env variables
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

TASK_NAME = "legal-aid"
BENCHMARK = "legal-aid-rl"
MAX_STEPS = 8
TEMPERATURE = 0.7
MAX_TOKENS = 150
SUCCESS_SCORE_THRESHOLD = 0.5

SYSTEM_PROMPT = textwrap.dedent("""
    You are a legal aid assistant helping users with legal problems.
    Each turn you will see the user's problem and collected info so far.
    
    You must respond with a JSON object with exactly two fields:
    - action_type: one of "ask_question", "suggest_action", "submit_solution"
    - content: your message or solution
    
    To collect required info, ask about it in your content.
    When ready, use submit_solution with the correct solution keyword.
    Reply with raw JSON only, no explanation.
""").strip()


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


def get_model_action(client: OpenAI, observation: dict, step: int, history: List[str]) -> dict:
    history_block = "\n".join(history[-4:]) if history else "None"
    user_prompt = textwrap.dedent(f"""
        Step: {step}
        User problem: {observation.get('user_problem', '')}
        Collected info: {observation.get('collected_info', {})}
        Progress: {observation.get('progress', 0.0)}
        Previous steps: {history_block}
        What is your next action?
    """).strip()

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        import json
        text = (completion.choices[0].message.content or "").strip()
        return json.loads(text)
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return {"action_type": "ask_question", "content": "Can you tell me the time and location?"}


async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    # Use local env directly
    env = LegalEnv(difficulty="easy")

    history: List[str] = []
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        obs = env.reset()
        last_obs = obs.model_dump()
        done = False

        for step in range(1, MAX_STEPS + 1):
            if done:
                break

            action_data = get_model_action(client, last_obs, step, history)
            action = Action(
                action_type=action_data.get("action_type", "ask_question"),
                content=action_data.get("content", "")
            )

            result = env.step(action)
            last_obs = result.observation.model_dump()
            reward = result.reward or 0.0
            done = result.done

            rewards.append(reward)
            steps_taken = step

            log_step(
                step=step,
                action=action.content[:50],
                reward=reward,
                done=done,
                error=None
            )

            history.append(f"Step {step}: {action.action_type} -> {action.content[:30]} reward={reward:.2f}")

        total_reward = sum(rewards)
        score = min(max(total_reward, 0.0), 1.0)
        success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as e:
        print(f"[DEBUG] Error: {e}", flush=True)

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())