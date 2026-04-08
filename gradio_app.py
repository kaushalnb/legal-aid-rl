import gradio as gr
from env.legal_env import LegalEnv   
from agent.baseline_agent import simple_agent
from env.tasks import TASKS

# global env (will be updated based on selection)
env = None
current_task = "easy"

def select_task(task_name):
    global env, current_task

    current_task = task_name
    env = LegalEnv(task_name)
    env.reset()

    return f"✅ Selected task: {task_name.upper()}. You can start chatting now!"

def chat(user_message, history):
    global env, current_task

    if history is None:
        history = []

    if env is None:
        return [("System", "⚠️ Please select a task first.")]

    state = env.state()

    action = simple_agent(state, TASKS[current_task])
    result = env.step(action)

    reply = f"{action.content}\n\n(Reward: {result.reward})"

    history.append((user_message, reply))
    return history

# UI Layout
with gr.Blocks() as demo:
    gr.Markdown("# ⚖️ AI Legal Assistant")
    gr.Markdown("Select a legal scenario and interact with the AI agent")

    with gr.Row():
        btn_easy = gr.Button("FIR Filing (Easy)")
        btn_medium = gr.Button("Consumer Complaint (Medium)")
        btn_hard = gr.Button("Property Dispute (Hard)")

    status = gr.Textbox(label="Status", interactive=False)

    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Describe your issue here...")

    msg.submit(chat, [msg, chatbot], chatbot)

    btn_easy.click(lambda: select_task("easy"), outputs=status)
    btn_medium.click(lambda: select_task("medium"), outputs=status)
    btn_hard.click(lambda: select_task("hard"), outputs=status)

demo.launch()