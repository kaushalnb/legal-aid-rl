from pydantic import BaseModel
from typing import Dict, Any

class Observation(BaseModel):
    user_problem: str
    collected_info: Dict[str, Any]
    progress: float

    class Config:
        arbitrary_types_allowed = True

class Action(BaseModel):
    action_type: str  # ask_question / suggest_action / submit_solution
    content: str

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]