from env.tasks import TASKS
from env.grader import compute_reward
from env.models import Observation, Action, StepResult

class LegalEnv:

    def __init__(self, difficulty="easy"):
        self.task = TASKS[difficulty]
        self.reset()

    def reset(self):
        self.state_data = {
            "user_problem": self.task["problem"],
            "collected_info": {},
            "progress": 0.0,
            "done": False
        }
        return Observation(**self.state_data)

    def step(self, action: Action):
        reward = compute_reward(self.state_data, action, self.task)

        # update progress
        collected = len(self.state_data["collected_info"])
        total = len(self.task["required_info"])
        self.state_data["progress"] = collected / total

        done = self.state_data["done"] or self.state_data["progress"] == 1.0

        obs = Observation(**self.state_data)

        return StepResult(
            observation=obs,
            reward=reward,
            done=done,
            info={}
        )

    def state(self):
        return self.state_data