from env.models import Action
import os
from openai import OpenAI

client = client = OpenAI(api_key="your_api_key_here")

def simple_agent(state, task):
    query = state["query"].lower()

    if "fir" in query:
        return "guide_fir"
    elif "consumer" in query:
        return "consumer_complaint"
    elif "property" in query:
        return "property_dispute"
    else:
        return "ask_clarification"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content

    # Decide action type
    if "?" in reply:
        action_type = "ask_question"
    else:
        action_type = "submit_solution"

    return Action(
        action_type=action_type,
        content=reply
    )