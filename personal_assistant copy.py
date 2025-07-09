# Step 1: Install required tools
# pip install openai fastapi uvicorn
# Install Ollama and download Phi-3 Mini: ollama run phi3

import json
import datetime
import os
from fastapi import FastAPI, Request
from openai import OpenAI

app = FastAPI()

# Step 2: Set up your personal memory (user_data.json)
USER_DATA_FILE = "user_data.json"

if not os.path.exists(USER_DATA_FILE):
    user_data = {
        "name": "Bhagya",
        "work_tasks": ["Prepare report", "Team meeting", "Client follow-up"],
        "personal_tasks": [],
        "family": ["Amma", "Thaththa", "Sister"],
        "family_events": [],
        "hobbies": ["Movies", "Music", "Reading"],
        "reminders": []
    }
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(user_data, f)
else:
    with open(USER_DATA_FILE, 'r') as f:
        user_data = json.load(f)

# Helper functions to save data
def save_user_data():
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(user_data, f, indent=2)

# Step 3: Add or view tasks, reminders, family events
def add_task(task):
    user_data.setdefault("personal_tasks", []).append(task)
    save_user_data()

def add_reminder(reminder):
    user_data.setdefault("reminders", []).append(reminder)
    save_user_data()

def add_family_event(event):
    user_data.setdefault("family_events", []).append(event)
    save_user_data()

def get_entertainment_recommendations():
    recommendations = {
        "Movies": ["Inception", "Interstellar", "The Matrix"],
        "Music": ["Classical", "Jazz", "Rock"],
        "Reading": ["1984 by Orwell", "The Hobbit", "Sapiens"]
    }
    recs = []
    for hobby in user_data.get("hobbies", []):
        recs.extend(recommendations.get(hobby, []))
    return recs

# Step 4: Personalize prompt
def personalize_prompt(user_input):
    name = user_data.get("name", "Friend")
    current_hour = datetime.datetime.now().hour

    greeting = f"Good morning {name}!" if current_hour < 12 else f"Good evening {name}!"

    all_tasks = user_data.get("work_tasks", []) + user_data.get("personal_tasks", [])
    reminders = user_data.get("reminders", [])
    family_events = user_data.get("family_events", [])

    task_list = ", ".join(all_tasks) or "No tasks found."
    reminder_list = ", ".join(reminders) or "No reminders."
    family_event_list = ", ".join(family_events) or "No family events scheduled."

    # Append personalized info if relevant keywords appear
    if "tasks" in user_input.lower():
        user_input += f" Here are your current tasks: {task_list}."
    if "reminder" in user_input.lower():
        user_input += f" Your reminders are: {reminder_list}."
    if "family event" in user_input.lower():
        user_input += f" Upcoming family events: {family_event_list}."
    if "recommend" in user_input.lower() or "entertainment" in user_input.lower():
        recs = get_entertainment_recommendations()
        user_input += f" Based on your hobbies, I recommend: {', '.join(recs)}."

    return f"{greeting} {user_input}"

# Step 5: Connect to local Ollama Phi-3 using new OpenAI client
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# Step 6: FastAPI Endpoint with enhanced command parsing
@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("prompt", "").strip()

    # Command handlers
    lower_input = user_input.lower()

    if lower_input.startswith("add task"):
        task = user_input[len("add task"):].strip()
        add_task(task)
        return {"response": f"Task '{task}' added to your personal tasks."}

    if lower_input.startswith("add reminder"):
        reminder = user_input[len("add reminder"):].strip()
        add_reminder(reminder)
        return {"response": f"Reminder '{reminder}' added."}

    if lower_input.startswith("add family event"):
        event = user_input[len("add family event"):].strip()
        add_family_event(event)
        return {"response": f"Family event '{event}' added."}

    # If no command, query LLM with personalized prompt
    prompt = personalize_prompt(user_input)

    response = client.chat.completions.create(
        model="phi3",
        messages=[
            {"role": "system", "content": "You are a helpful personal assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    reply = response.choices[0].message.content.strip()
    return {"response": reply}

# Step 7: Run the app
# Run this in your terminal:
# uvicorn personal_assistant:app --reload

# Example API calls:
# curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"prompt": "What are my tasks?"}'
# curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"prompt": "Add task buy groceries"}'
# curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"prompt": "Add reminder doctor appointment tomorrow"}'
# curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"prompt": "Add family event sister birthday"}'
# curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"prompt": "Recommend some entertainment"}'
