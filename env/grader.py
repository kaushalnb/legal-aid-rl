def compute_reward(state, action, task):
    reward = 0

    # reward for asking relevant info
    for key in task["required_info"]:
        if key in action.content.lower():
            if key not in state["collected_info"]:
                state["collected_info"][key] = True
                reward += 0.2

    # reward for correct solution
    if action.action_type == "submit_solution":
        if task["solution"] in action.content.lower():
            reward += 0.6
            state["done"] = True
        else:
            reward -= 0.3

    return reward