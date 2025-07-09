# Step 1: Install required tools
# pip install openai fastapi uvicorn
# Install Ollama and download Phi-3 Mini: ollama run phi3

import json
import datetime
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Step 2: Set up your personal memory (user_data.json)
USER_DATA_FILE = "user_data.json"

# Helper function to save data
def save_user_data():
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(user_data, f, indent=2)

if not os.path.exists(USER_DATA_FILE):
    user_data = {
        "name": "Bhagya",
        "tasks": [],  # Combined tasks instead of work_tasks and personal_tasks
        "family": ["Amma", "Thaththa", "Sister"],
        "reminders": [],
        "schedule": {},
        "contacts": {},
        "notes": [],
        "goals": [],  # Simplified goals without categories
        "expenses": [],
        "preferences": {
            "work_hours": "9:00-17:00",
            "timezone": "UTC+5:30",
            "notification_style": "gentle"
        }
    }
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(user_data, f)
else:
    with open(USER_DATA_FILE, 'r') as f:
        user_data = json.load(f)
    
    # Migrate old data structure to new simplified structure
    if "work_tasks" in user_data or "personal_tasks" in user_data:
        print("Migrating data to new structure...")
        # Combine work_tasks and personal_tasks into tasks
        all_tasks = user_data.get("work_tasks", []) + user_data.get("personal_tasks", [])
        user_data["tasks"] = all_tasks
        
        # Combine goals if they're in category format
        if isinstance(user_data.get("goals", {}), dict):
            all_goals = []
            for category, goal_list in user_data.get("goals", {}).items():
                for goal in goal_list:
                    all_goals.append(f"{category}: {goal}" if category else goal)
            user_data["goals"] = all_goals
        
        # Remove old keys
        user_data.pop("work_tasks", None)
        user_data.pop("personal_tasks", None)
        user_data.pop("family_events", None)
        user_data.pop("hobbies", None)
        user_data.pop("habits", None)
        
        # Save migrated data
        save_user_data()
        print("Data migration completed!")

# Step 3: Simplified data management functions

# Validation functions to prevent dummy/test/duplicate data
def is_valid_content(content, min_length=2):
    """Check if content is valid (not dummy/test data)"""
    if not content or len(content.strip()) < min_length:
        return False
    
    content_lower = content.strip().lower()
    
    # Block single characters and very short dummy entries
    if len(content_lower) <= 1:
        return False
    
    # Block common dummy/test patterns
    dummy_patterns = [
        'test', 'dummy', 'sample', 'example', 'kill', 'delete', 'remove',
        'xxx', 'yyy', 'zzz', 'abc', 'asdf', 'qwerty', '123', 'temp',
        'placeholder', 'lorem', 'ipsum', 'hello world', 'testing'
    ]
    
    # Block if content is entirely a dummy pattern
    if content_lower in dummy_patterns:
        return False
    
    # Block if content starts with dummy patterns (like "test reminder")
    for pattern in ['test ', 'dummy ', 'sample ', 'example ']:
        if content_lower.startswith(pattern):
            return False
    
    return True

def is_duplicate(content, existing_list):
    """Check if content already exists in the list"""
    if not existing_list:
        return False
    
    content_lower = content.strip().lower()
    for item in existing_list:
        if isinstance(item, str) and item.strip().lower() == content_lower:
            return True
        elif isinstance(item, dict) and 'description' in item:
            if item['description'].strip().lower() == content_lower:
                return True
    return False

def add_task(task):
    task = task.strip()
    if not is_valid_content(task, min_length=3):
        return False, "Invalid task: too short or appears to be test data"
    
    existing_tasks = user_data.get("tasks", [])
    if is_duplicate(task, existing_tasks):
        return False, "Task already exists"
    
    user_data.setdefault("tasks", []).append(task)
    save_user_data()
    return True, "Task added successfully"

def complete_task(task_name):
    # Remove from tasks list
    if task_name in user_data.get("tasks", []):
        user_data["tasks"].remove(task_name)
        save_user_data()
        return True
    return False

def add_reminder(reminder):
    reminder = reminder.strip()
    if not is_valid_content(reminder, min_length=3):
        return False, "Invalid reminder: too short or appears to be test data"
    
    existing_reminders = user_data.get("reminders", [])
    if is_duplicate(reminder, existing_reminders):
        return False, "Reminder already exists"
    
    user_data.setdefault("reminders", []).append(reminder)
    save_user_data()
    return True, "Reminder added successfully"

def add_schedule_item(date, item):
    item = item.strip()
    if not is_valid_content(item, min_length=3):
        return False, "Invalid schedule item: too short or appears to be test data"
    
    existing_items = user_data.get("schedule", {}).get(date, [])
    if is_duplicate(item, existing_items):
        return False, "Schedule item already exists for this date"
    
    user_data.setdefault("schedule", {}).setdefault(date, []).append(item)
    save_user_data()
    return True, "Schedule item added successfully"

def add_contact(name, info):
    name = name.strip()
    info = info.strip()
    
    if not is_valid_content(name, min_length=2):
        return False, "Invalid contact name: too short or appears to be test data"
    
    if not is_valid_content(info, min_length=3):
        return False, "Invalid contact info: too short or appears to be test data"
    
    # Check if contact already exists
    existing_contacts = user_data.get("contacts", {})
    if name in existing_contacts:
        return False, "Contact already exists"
    
    user_data.setdefault("contacts", {})[name] = info
    save_user_data()
    return True, "Contact added successfully"

def add_note(note):
    note = note.strip()
    if not is_valid_content(note, min_length=3):
        return False, "Invalid note: too short or appears to be test data"
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    note_with_timestamp = f"[{timestamp}] {note}"
    
    # Check for duplicate notes (without timestamp)
    existing_notes = user_data.get("notes", [])
    for existing_note in existing_notes:
        # Extract content without timestamp for comparison
        if "] " in existing_note:
            existing_content = existing_note.split("] ", 1)[1]
            if existing_content.strip().lower() == note.lower():
                return False, "Note with similar content already exists"
    
    user_data.setdefault("notes", []).append(note_with_timestamp)
    save_user_data()
    return True, "Note added successfully"

def add_goal(goal):
    goal = goal.strip()
    if not is_valid_content(goal, min_length=3):
        return False, "Invalid goal: too short or appears to be test data"
    
    existing_goals = user_data.get("goals", [])
    if is_duplicate(goal, existing_goals):
        return False, "Goal already exists"
    
    user_data.setdefault("goals", []).append(goal)
    save_user_data()
    return True, "Goal added successfully"

def add_expense(amount, description, category="misc"):
    description = description.strip()
    
    # Validate amount
    try:
        amount_float = float(amount)
        if amount_float <= 0 or amount_float > 10000:  # Reasonable limits
            return False, "Invalid amount: must be between 0 and 10000"
    except (ValueError, TypeError):
        return False, "Invalid amount: must be a valid number"
    
    if not is_valid_content(description, min_length=3):
        return False, "Invalid expense description: too short or appears to be test data"
    
    # Check for recent duplicate expenses (same description, similar amount, same day)
    existing_expenses = user_data.get("expenses", [])
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    for expense in existing_expenses:
        if (expense.get("description", "").strip().lower() == description.lower() and 
            expense.get("date") == today and 
            abs(float(expense.get("amount", 0)) - amount_float) < 0.01):
            return False, "Similar expense already recorded today"
    
    expense = {
        "amount": amount_float,
        "description": description,
        "category": category,
        "date": today
    }
    user_data.setdefault("expenses", []).append(expense)
    save_user_data()
    return True, "Expense added successfully"

def get_today_schedule():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return user_data.get("schedule", {}).get(today, [])

def get_expense_summary():
    total = sum(float(expense["amount"]) for expense in user_data.get("expenses", []))
    return f"Total expenses: ${total:.2f}"

# Step 4: Simplified AI-enhanced prompt processing

def personalize_prompt(user_input):
    name = user_data.get("name", "Friend")
    lower_input = user_input.lower()

    # Family queries
    if any(pattern in lower_input for pattern in ["family", "show family", "my family", "who is my family", "family members", "list family"]):
        family = user_data.get("family", [])
        if family:
            return f"Your family: {', '.join(family)}"
        else:
            return "No family members saved."
    
    # Contact queries
    if any(pattern in lower_input for pattern in ["contact", "contacts", "my contacts", "what are my contacts", "list contacts", "all contacts", "show contact"]):
        contacts = user_data.get("contacts", {})
        if contacts:
            contact_list = []
            for name, info in contacts.items():
                contact_list.append(f"{name}: {info}")
            return f"Your contacts: {'; '.join(contact_list)}"
        else:
            return "No contacts saved."

    # Individual contact lookup
    contacts = user_data.get("contacts", {})
    for contact_name in contacts.keys():
        if any(pattern in lower_input for pattern in [
            f"{contact_name.lower()}'s contact",
            f"{contact_name.lower()} contact", 
            f"give {contact_name.lower()}",
            f"show {contact_name.lower()}",
            f"find {contact_name.lower()}",
            f"get {contact_name.lower()}",
            f"{contact_name.lower()} number",
            f"{contact_name.lower()} phone",
            f"{contact_name.lower()} email"
        ]):
            return f"{contact_name}: {contacts[contact_name]}"

    # Task queries - simplified to single category
    if any(pattern in lower_input for pattern in ["task", "tasks", "my tasks", "what are my tasks", "show tasks", "list tasks", "all tasks"]):
        tasks = user_data.get("tasks", [])
        task_list = ", ".join(tasks) or "No tasks."
        return f"Your current tasks: {task_list}"

    # Schedule queries
    if any(pattern in lower_input for pattern in ["schedule", "today", "my schedule", "what's my schedule", "today's schedule", "show schedule"]):
        today_schedule = get_today_schedule()
        if today_schedule:
            return f"Today's schedule: {', '.join(today_schedule)}"
        else:
            return "No items scheduled for today."

    # Reminder queries
    if any(pattern in lower_input for pattern in ["reminder", "reminders", "my reminders", "what are my reminders", "show reminders", "list reminders"]):
        reminders = user_data.get("reminders", [])
        reminder_list = ", ".join(reminders) or "No reminders."
        return f"Your reminders: {reminder_list}"

    # Notes queries
    if any(pattern in lower_input for pattern in ["note", "notes", "my notes", "show notes", "list notes"]):
        recent_notes = user_data.get("notes", [])[-5:]  # Last 5 notes
        if recent_notes:
            return f"Recent notes: {'; '.join(recent_notes)}"
        else:
            return "No notes saved."

    # Goals queries - simplified
    if any(pattern in lower_input for pattern in ["goal", "goals", "my goals", "show goals", "list goals"]):
        goals = user_data.get("goals", [])
        if goals:
            return f"Your goals: {'; '.join(goals)}"
        else:
            return "No goals set."

    # Expense queries
    if any(pattern in lower_input for pattern in ["expense", "expenses", "money", "budget", "spending"]):
        return get_expense_summary()

    # If no clear pattern is matched, let AI handle it with context
    return f"AI_CONTEXT: {user_input} | User: {name} | Available data: tasks, family, contacts, reminders, schedule, notes, goals, expenses"

# Step 5: Connect to local Ollama Phi-3
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# Step 6: FastAPI Endpoint

@app.post("/chat")
async def chat(request: Request):
    import re  # Move import to the top of the function
    body = await request.json()
    user_input = body.get("prompt", "").strip()
    lower_input = user_input.lower()

    # Quick greetings
    if lower_input in ["good morning", "good afternoon", "good evening"]:
        name = user_data.get("name", "Friend")
        today_tasks = len(user_data.get("tasks", []))
        today_schedule = get_today_schedule()
        schedule_msg = f"You have {len(today_schedule)} scheduled items today." if today_schedule else "No scheduled items today."
        return {"response": f"Good morning, {name}! You have {today_tasks} pending tasks. {schedule_msg}"}

    # TASK COMPLETION - Enhanced Natural Language (process early to avoid conflicts)
    # Natural language task completion: "completed buy groceries", "finished the report", "done with meeting", etc.
    if any(word in lower_input for word in ["complete", "completed", "finish", "finished", "done"]):
        completion_patterns = [
            r'(?:completed?|finished?|done)\s+(?:task\s+)?(.+)',        # "completed buy groceries"
            r'(?:completed?|finished?|done)\s+(?:with\s+)?(.+)',        # "done with meeting"
            r'mark\s+(?:task\s+)?(.+?)\s+(?:as\s+)?(?:done|complete)',  # "mark task buy groceries as done"
            r'(?:task\s+)?(.+?)\s+(?:is\s+)?(?:done|complete)',         # "buy groceries is done"
        ]
        
        for pattern in completion_patterns:
            match = re.search(pattern, lower_input)
            if match:
                task_content = match.group(1).strip()
                if task_content and not any(word in task_content for word in ["complete", "completed", "finish", "finished", "done", "mark", "task"]):
                    if complete_task(task_content):
                        return {"response": f"Task '{task_content}' marked as complete!"}
                    else:
                        return {"response": f"Task '{task_content}' not found in your task list."}
        
        # Traditional format
        for pattern in ["complete task:", "finish task:", "done task:", "mark task complete:"]:
            if pattern in lower_input:
                task_content = user_input[user_input.lower().find(pattern) + len(pattern):].strip()
                if task_content and complete_task(task_content):
                    return {"response": f"Task '{task_content}' marked as complete!"}
                elif task_content:
                    return {"response": f"Task '{task_content}' not found in your task list."}

    # Enhanced natural language processing for all operations
    
    # CONTACT OPERATIONS - Natural Language
    # Add contact with natural language (phone/email detection)
    if any(word in lower_input for word in ["phone", "number", "email"]) and any(word in lower_input for word in ["add", "create"]):
        # Extract name (usually the first word after "add")
        name_match = re.search(r'add\s+(\w+)', lower_input)
        name = name_match.group(1) if name_match else None
        
        # Extract phone number (sequence of digits)
        phone_match = re.search(r'(\d{8,})', user_input)
        phone = phone_match.group(1) if phone_match else None
        
        # Extract email
        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', user_input)
        email = email_match.group(1) if email_match else None
        
        if name and (phone or email):
            contact_info = ""
            if phone and email:
                contact_info = f"{phone}, {email}"
            elif phone:
                contact_info = phone
            elif email:
                contact_info = email
            
            success, message = add_contact(name.capitalize(), contact_info)
            if success:
                return {"response": f"Contact '{name.capitalize()}' added successfully with {contact_info}!"}
            else:
                return {"response": f"Failed to add contact: {message}"}
    
    # TASK OPERATIONS - Enhanced Natural Language
    # Natural language task addition: "add task to buy groceries", "create task call doctor", etc.
    if any(word in lower_input for word in ["task", "todo"]) and any(word in lower_input for word in ["add", "create", "new"]):
        task_patterns = [
            r'(?:add|create|new)\s+(?:task|todo)\s+to\s+(.+)',  # "add task to buy groceries"
            r'(?:add|create|new)\s+(?:task|todo)\s+(.+)',       # "add task buy groceries"
            r'(?:add|create|new)\s+(.+)\s+(?:task|todo)',       # "add buy groceries task"
        ]
        
        for pattern in task_patterns:
            match = re.search(pattern, lower_input)
            if match:
                task_content = match.group(1).strip()
                if task_content and not any(word in task_content for word in ["add", "create", "new", "task", "todo"]):
                    success, message = add_task(task_content)
                    if success:
                        return {"response": f"Task '{task_content}' added successfully!"}
                    else:
                        return {"response": f"Failed to add task: {message}"}
        
        # Fallback to traditional patterns
        for pattern in ["add new task:", "add task:", "create task:", "new task:"]:
            if pattern in lower_input:
                task_content = user_input[user_input.lower().find(pattern) + len(pattern):].strip()
                if task_content:
                    success, message = add_task(task_content)
                    if success:
                        return {"response": f"Task '{task_content}' added successfully!"}
                    else:
                        return {"response": f"Failed to add task: {message}"}
        
        for pattern in ["add new task", "add task", "create task", "new task"]:
            if pattern in lower_input:
                task_content = user_input[user_input.lower().find(pattern) + len(pattern):].strip()
                if task_content:
                    success, message = add_task(task_content)
                    if success:
                        return {"response": f"Task '{task_content}' added successfully!"}
                    else:
                        return {"response": f"Failed to add task: {message}"}
        
        return {"response": "Please specify the task. Example: 'add task to buy groceries' or 'create task call doctor'"}
    
    # REMINDER OPERATIONS - Enhanced Natural Language
    # Natural language reminders: "remind me to call mom", "add reminder to buy milk", etc.
    if any(word in lower_input for word in ["remind", "reminder"]) and any(word in lower_input for word in ["add", "create", "new", "me"]):
        reminder_patterns = [
            r'remind\s+me\s+to\s+(.+)',                        # "remind me to call mom"
            r'(?:add|create|new)\s+reminder\s+to\s+(.+)',      # "add reminder to buy milk"
            r'(?:add|create|new)\s+reminder\s+(.+)',           # "add reminder call mom"
        ]
        
        for pattern in reminder_patterns:
            match = re.search(pattern, lower_input)
            if match:
                reminder_content = match.group(1).strip()
                if reminder_content and not any(word in reminder_content for word in ["add", "create", "new", "remind", "reminder"]):
                    success, message = add_reminder(reminder_content)
                    if success:
                        return {"response": f"Reminder '{reminder_content}' added successfully!"}
                    else:
                        return {"response": f"Failed to add reminder: {message}"}
        
        # Fallback to traditional patterns
        for pattern in ["add new reminder:", "add reminder:", "create reminder:", "remind me:"]:
            if pattern in lower_input:
                reminder_content = user_input[user_input.lower().find(pattern) + len(pattern):].strip()
                if reminder_content:
                    success, message = add_reminder(reminder_content)
                    if success:
                        return {"response": f"Reminder '{reminder_content}' added successfully!"}
                    else:
                        return {"response": f"Failed to add reminder: {message}"}
        
        return {"response": "Please specify the reminder. Example: 'remind me to call mom' or 'add reminder to buy milk'"}
    
    # GOAL OPERATIONS - Enhanced Natural Language
    # Natural language goals: "add goal to learn spanish", "add a goal to cycle", "create goal exercise daily", etc.
    if any(word in lower_input for word in ["goal", "objective"]) and any(word in lower_input for word in ["add", "create", "new", "set"]):
        goal_patterns = [
            r'(?:add|create|new|set)\s+(?:a\s+)?goal\s+to\s+(.+)',       # "add goal to learn spanish" or "add a goal to cycle"
            r'(?:add|create|new|set)\s+(?:a\s+)?goal\s+(.+)',            # "add goal learn spanish" or "add a goal exercise"
            r'(?:add|create|new|set)\s+(.+)\s+goal',                     # "add learn spanish goal"
            r'(?:set|add)\s+(?:a\s+)?(.+)\s+(?:as\s+)?(?:goal|objective)', # "set cycle as goal"
        ]
        
        for pattern in goal_patterns:
            match = re.search(pattern, lower_input)
            if match:
                goal_content = match.group(1).strip()
                # Filter out common words only if they are the entire content or at the beginning
                if goal_content and goal_content.lower() not in ["add", "create", "new", "set", "goal", "objective", "a", "an", "the"]:
                    success, message = add_goal(goal_content)
                    if success:
                        return {"response": f"Goal '{goal_content}' added successfully!"}
                    else:
                        return {"response": f"Failed to add goal: {message}"}
        
        # Fallback to traditional patterns
        for pattern in ["add new goal:", "add goal:", "create goal:", "set goal:"]:
            if pattern in lower_input:
                goal_content = user_input[user_input.lower().find(pattern) + len(pattern):].strip()
                if goal_content:
                    success, message = add_goal(goal_content)
                    if success:
                        return {"response": f"Goal '{goal_content}' added successfully!"}
                    else:
                        return {"response": f"Failed to add goal: {message}"}
        
        return {"response": "Please specify the goal. Example: 'add goal to exercise daily' or 'set goal learn spanish'"}
    
    # CONTACT OPERATIONS - Traditional Format
    if any(pattern in lower_input for pattern in ["add contact", "add new contact", "create contact"]):
        # Handle multiple contact formats
        contact_added = False
        
        # Format 1: "add contact Name: phone/email"
        if ":" in user_input:
            for pattern in ["add new contact", "add contact", "create contact"]:
                if pattern in lower_input:
                    contact_part = user_input[user_input.lower().find(pattern) + len(pattern):].strip()
                    if ":" in contact_part:
                        parts = contact_part.split(":", 1)
                        if len(parts) == 2:
                            name = parts[0].strip()
                            info = parts[1].strip()
                            success, message = add_contact(name, info)
                            if success:
                                return {"response": f"Contact '{name}' added successfully!"}
                            else:
                                return {"response": f"Failed to add contact: {message}"}
        
        return {"response": "Please specify contact details. Examples: 'add contact John: 123-456-7890' or 'add Johns phone number 123456789'"}
    
    # NOTE OPERATIONS - Enhanced Natural Language
    # Natural language notes: "add note about meeting", "create note important info", "note that ...", etc.
    if any(word in lower_input for word in ["note", "notes"]) and any(word in lower_input for word in ["add", "create", "new", "save", "record"]):
        note_patterns = [
            r'(?:add|create|new|save|record)\s+note\s+about\s+(.+)',    # "add note about meeting"
            r'(?:add|create|new|save|record)\s+note\s+that\s+(.+)',     # "add note that important"
            r'(?:add|create|new|save|record)\s+note\s+(.+)',            # "add note meeting details"
            r'note\s+that\s+(.+)',                                      # "note that meeting is important"
            r'note\s+(.+)',                                             # "note meeting details"
        ]
        
        for pattern in note_patterns:
            match = re.search(pattern, lower_input)
            if match:
                note_content = match.group(1).strip()
                if note_content and not any(word in note_content for word in ["add", "create", "new", "save", "record", "note"]):
                    success, message = add_note(note_content)
                    if success:
                        return {"response": f"Note added successfully!"}
                    else:
                        return {"response": f"Failed to add note: {message}"}
        
        # Fallback to traditional patterns
        for pattern in ["add new note:", "add note:", "create note:", "save note:"]:
            if pattern in lower_input:
                note_content = user_input[user_input.lower().find(pattern) + len(pattern):].strip()
                if note_content:
                    success, message = add_note(note_content)
                    if success:
                        return {"response": f"Note added successfully!"}
                    else:
                        return {"response": f"Failed to add note: {message}"}
        
        return {"response": "Please specify the note. Example: 'add note about meeting' or 'note that important info'"}
    
    # EXPENSE OPERATIONS - Enhanced Natural Language
    # Natural language expenses: "add expense 25 for lunch", "spent 50 on groceries", "record expense 30 for gas", etc.
    if any(word in lower_input for word in ["expense", "spent", "cost", "paid"]) and any(word in lower_input for word in ["add", "record", "create"]) or \
       any(phrase in lower_input for phrase in ["spent", "paid", "cost me"]):
        
        expense_patterns = [
            r'(?:add|record|create)\s+expense\s+(\d+(?:\.\d{2})?)\s+for\s+(.+)',    # "add expense 25 for lunch"
            r'(?:add|record|create)\s+expense\s+(\d+(?:\.\d{2})?)\s+(.+)',          # "add expense 25 lunch"
            r'spent\s+(\d+(?:\.\d{2})?)\s+on\s+(.+)',                              # "spent 50 on groceries"
            r'paid\s+(\d+(?:\.\d{2})?)\s+for\s+(.+)',                             # "paid 30 for gas"
            r'cost\s+me\s+(\d+(?:\.\d{2})?)\s+for\s+(.+)',                        # "cost me 20 for coffee"
            r'(\d+(?:\.\d{2})?)\s+(?:for|on)\s+(.+)',                             # "25 for lunch"
        ]
        
        for pattern in expense_patterns:
            match = re.search(pattern, lower_input)
            if match:
                amount = match.group(1).strip()
                description = match.group(2).strip()
                if amount and description and not any(word in description for word in ["add", "record", "create", "expense"]):
                    success, message = add_expense(amount, description)
                    if success:
                        return {"response": f"Expense of ${amount} for '{description}' recorded successfully!"}
                    else:
                        return {"response": f"Failed to record expense: {message}"}
        
        # Traditional format with colon
        if ":" in user_input:
            for pattern in ["add new expense", "add expense", "record expense"]:
                if pattern in lower_input:
                    expense_part = user_input[user_input.lower().find(pattern) + len(pattern):].strip()
                    if ":" in expense_part:
                        parts = expense_part.split(":", 1)
                        if len(parts) == 2:
                            amount = parts[0].strip()
                            description = parts[1].strip()
                            success, message = add_expense(amount, description)
                            if success:
                                return {"response": f"Expense of ${amount} for '{description}' recorded successfully!"}
                            else:
                                return {"response": f"Failed to record expense: {message}"}
        
        return {"response": "Please specify the expense. Example: 'add expense 25 for lunch' or 'spent 50 on groceries'"}
    
    # SCHEDULE OPERATIONS - Enhanced Natural Language
    # Natural language scheduling: "schedule meeting tomorrow", "add appointment on 2025-07-15", etc.
    if any(word in lower_input for word in ["schedule", "appointment", "meeting"]) and any(word in lower_input for word in ["add", "create", "set", "book"]) or \
       any(phrase in lower_input for phrase in ["schedule for", "book on", "set appointment"]):
        
        schedule_patterns = [
            r'(?:schedule|add|create|set|book)\s+(.+?)\s+(?:on|for)\s+(\d{4}-\d{2}-\d{2})',     # "schedule meeting on 2025-07-15"
            r'(?:schedule|add|create|set|book)\s+(.+?)\s+(?:tomorrow|today)',                     # "schedule meeting tomorrow"
            r'(?:schedule|add|create|set|book)\s+appointment\s+(.+?)\s+(?:on|for)\s+(\d{4}-\d{2}-\d{2})', # "book appointment dentist on 2025-07-15"
        ]
        
        # Handle "tomorrow" and "today"
        if "tomorrow" in lower_input:
            from datetime import datetime, timedelta
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            event_match = re.search(r'(?:schedule|add|create|set|book)\s+(.+?)\s+tomorrow', lower_input)
            if event_match:
                event = event_match.group(1).strip()
                success, message = add_schedule_item(tomorrow, event)
                if success:
                    return {"response": f"Scheduled '{event}' for tomorrow ({tomorrow})"}
                else:
                    return {"response": f"Failed to schedule: {message}"}
        
        if "today" in lower_input:
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            event_match = re.search(r'(?:schedule|add|create|set|book)\s+(.+?)\s+today', lower_input)
            if event_match:
                event = event_match.group(1).strip()
                success, message = add_schedule_item(today, event)
                if success:
                    return {"response": f"Scheduled '{event}' for today ({today})"}
                else:
                    return {"response": f"Failed to schedule: {message}"}
        
        # Handle specific dates
        for pattern in schedule_patterns:
            match = re.search(pattern, lower_input)
            if match:
                if len(match.groups()) == 2:
                    event = match.group(1).strip()
                    date = match.group(2).strip()
                    success, message = add_schedule_item(date, event)
                    if success:
                        return {"response": f"Scheduled '{event}' for {date}"}
                    else:
                        return {"response": f"Failed to schedule: {message}"}
        
        # Traditional format with colon
        if ":" in user_input:
            parts = user_input.split(":", 1)
            if len(parts) == 2:
                # Find potential date in the first part
                words = parts[0].split()
                date_part = None
                for word in words:
                    if "-" in word and len(word) >= 8:  # Basic date format check YYYY-MM-DD
                        date_part = word
                        break
                
                if date_part:
                    event = parts[1].strip()
                    success, message = add_schedule_item(date_part, event)
                    if success:
                        return {"response": f"Scheduled '{event}' for {date_part}"}
                    else:
                        return {"response": f"Failed to schedule: {message}"}
        
        return {"response": "Please specify the schedule. Example: 'schedule meeting tomorrow' or 'book appointment on 2025-07-15'"}

    # ENHANCED LOOKUP/VIEW OPERATIONS - Natural Language
    # Enhanced individual contact lookup for natural language
    if any(pattern in lower_input for pattern in ["show", "find", "get"]) and "contact" in lower_input:
        # First check if it's asking for all contacts
        if any(all_contact_pattern in lower_input for all_contact_pattern in ["show contacts", "list contacts", "all contacts", "my contacts"]):
            # Let it fall through to the general pattern matching in personalize_prompt
            pass
        else:
            # Extract potential name from the query
            name_patterns = [
                r'(?:show|find|get)\s+(\w+)\s+contact',
                r'(?:show|find|get)\s+(\w+)\s+(?:phone|number|email)',
                r'(?:show|find|get)\s+(\w+)(?:\s|$)'
            ]
            
            query_name = None
            for pattern in name_patterns:
                match = re.search(pattern, lower_input)
                if match:
                    query_name = match.group(1).lower()
                    break
            
            if query_name and query_name not in ["contacts", "contact", "phone", "number", "email"]:
                contacts = user_data.get("contacts", {})
                # Look for exact match or partial match
                for contact_name, contact_info in contacts.items():
                    if query_name == contact_name.lower() or query_name in contact_name.lower():
                        return {"response": f"{contact_name}: {contact_info}"}
                
                # If no match found
                return {"response": f"No contact found for '{query_name}'. Available contacts: {', '.join(contacts.keys())}"}

    # Try to get response from personalized patterns for VIEW operations
    prompt = personalize_prompt(user_input)
    
    # If it's a direct data response, return it immediately
    if not prompt.startswith("AI_CONTEXT:"):
        return {"response": prompt}

    # If no clear pattern matched, use AI with enhanced context
    try:
        system_prompt = f"""You are {user_data.get('name', 'Bhagya')}'s intelligent personal assistant. 

CURRENT DATA:
- Tasks: {user_data.get('tasks', [])}
- Family: {user_data.get('family', [])}
- Contacts: {list(user_data.get('contacts', {}).keys())}
- Reminders: {user_data.get('reminders', [])}
- Goals: {user_data.get('goals', [])}

RESPONSE STYLE:
- Be conversational and helpful
- Give SHORT, direct answers (1-2 sentences max)
- If the query is completely unrelated to personal management, say: "I'm here to help with your tasks, contacts, schedule, and personal information. What would you like to manage today?"

Current query: {user_input}"""

        response = client.chat.completions.create(
            model="phi3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        
        ai_response = response.choices[0].message.content.strip()
        return {"response": ai_response}
        
    except Exception as e:
        return {"response": "I'm having trouble connecting to my AI service. Please try again later."}

# Step 7: Run the app
# uvicorn personal_assistant:app --reload
