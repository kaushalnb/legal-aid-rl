from agent.baseline_agent import simple_agent
from env.tasks import TASKS
from env.legal_env import LegalEnv

def run_task(level):
    env = LegalEnv(level)
    obs = env.reset()

    total_reward = 0

    for _ in range(5):
        action = simple_agent(env.state(), TASKS[level])
        print("Action:", action)

        result = env.step(action)
        print("Reward:", result.reward)
        print("State:", result.observation)

        total_reward += result.reward

        if result.done:
            break

    return total_reward


if __name__ == "__main__":
    scores = {}
    for level in ["easy", "medium", "hard"]:
        score = run_task(level)
        scores[level] = score
        print(f"{level}: {score}")

    print("Final Score:", sum(scores.values()) / 3)