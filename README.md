# Bhagya's Personal Assistant - User Guide

## 🚀 Getting Started

1. **Start the server:**
   ```bash
   cd /Users/bhagya/Desktop/chatbot
   uvicorn personal_assistant:app --reload
   ```

2. **Open the frontend:**
   Open `frontend.html` in your web browser or use the API directly at `http://localhost:8000/chat`

## 📋 Features & Commands

### Task Management
- `add task: Buy groceries` - Add a personal task
- `add work task: Prepare presentation` - Add a work-specific task
- `complete task: Buy groceries` - Mark a task as complete
- `show tasks` - View all tasks
- `show work tasks` - View only work tasks

### 📅 Schedule Management
- `schedule 2025-07-10: Doctor appointment` - Add to specific date
- `show today` - View today's schedule
- `show schedule` - View all scheduled items

### 📝 Notes & Reminders
- `add note: Remember to call mom` - Quick note with timestamp
- `add reminder: Pay electricity bill` - Add a reminder
- `show notes` - View recent notes
- `show reminders` - View all reminders

### 👨‍👩‍👧‍👦 Family & Personal
- `add family event: Sister's birthday party` - Add family events
- `show family events` - View family events
- `show family` - View family members

### 💰 Expense Tracking
- `add expense 50: Lunch at restaurant` - Track expenses
- `show expenses` - View expense summary
- `show budget` - Same as show expenses

### 🎯 Goals & Habits
- `add goal work: Complete project by month end` - Add work goal
- `add goal personal: Read 2 books this month` - Add personal goal
- `add goal health: Exercise 3 times per week` - Add health goal
- `add habit: Morning meditation` - Track a habit
- `show goals` - View all goals
- `show habits` - View tracked habits

### 📱 Contacts
- `add contact John Doe: 123-456-7890` - Add contact with phone
- `add contact Jane Smith: jane@email.com` - Add contact with email
- `show contacts` - View all contacts

### 🌟 Quick Actions
- `good morning` - Get morning summary
- `good afternoon` - Get afternoon greeting
- `good evening` - Get evening greeting
- `motivation` - Get motivational quote
- `weather` - Weather reminder
- `recommend entertainment` - Get entertainment suggestions

### 💬 Natural Conversation
Your assistant also responds to natural language:
- "What do I have planned today?"
- "How much money have I spent?"
- "What are my current goals?"
- "Show me my family events"
- "I need some motivation"

## 🎨 Customization

### Personal Information
Edit the `user_data.json` file to customize:
- Your name
- Family members
- Hobbies and interests
- Work preferences
- Default tasks

### Adding New Features
The assistant is built to be easily extensible. You can add new commands by:
1. Adding new data fields to the user_data structure
2. Creating new helper functions
3. Adding command recognition in the chat endpoint
4. Updating the personalize_prompt function

## 🔧 Technical Details

### Data Storage
All your data is stored locally in `user_data.json` including:
- Tasks (work and personal)
- Schedule items
- Notes with timestamps
- Contacts
- Expenses
- Goals by category
- Habits
- Family events
- Reminders

### API Integration
- Uses Ollama with Phi-3 model for AI responses
- FastAPI backend for handling requests
- Simple HTML frontend for easy interaction

### Privacy
- All data stays on your local machine
- No external services except for the local Ollama instance
- You have full control over your personal information

## 🎯 Best Practices

1. **Daily Check-ins:** Start your day with "good morning" to get an overview
2. **Regular Updates:** Add tasks and events as they come up
3. **Goal Tracking:** Review goals weekly and update progress
4. **Expense Monitoring:** Log expenses immediately for better tracking
5. **Schedule Planning:** Use the schedule feature for time management

## 🛠️ Troubleshooting

- **Server not starting:** Make sure Ollama is running and Phi-3 is installed
- **AI not responding:** Check if Ollama service is active
- **Data not saving:** Ensure write permissions in the chatbot directory
- **Frontend not connecting:** Verify the server is running on localhost:8000

## 🚀 Future Enhancements

Consider adding:
- Weather API integration
- Calendar sync
- Email notifications
- Voice commands
- Mobile app
- Data export/backup features
- Integration with other productivity tools

---

Enjoy your personalized digital assistant! 🤖✨
