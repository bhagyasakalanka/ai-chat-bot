# Personal Assistant Chatbot

A natural language-powered personal assistant that helps you manage tasks, contacts, reminders, goals, expenses, notes, and scheduling through an intelligent conversational interface.

## Features

- 🗣️ **Natural Language Processing**: Supports conversational commands like "add task to buy groceries" or "remind me to call mom"
- ✅ **Task Management**: Create, complete, and track tasks with intelligent completion detection
- 👥 **Contact Management**: Store and retrieve contact information with phone/email auto-detection
- 💰 **Expense Tracking**: Log expenses with natural language ("spent 25 on lunch")
- 🎯 **Goal Setting**: Set and track personal and professional goals
- 📝 **Note Taking**: Quick note capture with timestamps
- 📅 **Schedule Management**: Add appointments and view daily schedules
- 🛡️ **Data Validation**: Prevents dummy/test data and duplicates
- 🤖 **AI-Powered**: Local AI integration for intelligent responses
- 🔒 **Privacy-First**: All data stored locally, no cloud dependencies

## Technology Stack

- **Backend**: FastAPI (Python)
- **AI**: Ollama + Phi-3 Mini (Local LLM)
- **Frontend**: HTML/CSS/JavaScript
- **Storage**: JSON file-based
- **NLP**: Regex pattern matching + AI fallback

## Prerequisites

- Python 3.8 or higher
- macOS, Linux, or Windows
- At least 4GB RAM (for AI model)
- Internet connection (for initial setup only)

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd chatbot
```

### Step 2: Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv gpt-assistant-env

# Activate virtual environment
# On macOS/Linux:
source gpt-assistant-env/bin/activate

# On Windows:
gpt-assistant-env\Scripts\activate
```

### Step 3: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install fastapi uvicorn openai python-multipart
```

### Step 4: Install and Set Up Ollama

#### On macOS:
```bash
# Install Ollama using Homebrew
brew install ollama

# Or download from https://ollama.ai/download
```

#### On Linux:
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
```

#### On Windows:
1. Download the Ollama installer from https://ollama.ai/download
2. Run the installer and follow the setup wizard

### Step 5: Start Ollama Service

```bash
# Start Ollama service (run in a separate terminal)
ollama serve
```

### Step 6: Download Phi-3 Mini Model

```bash
# Download and set up Phi-3 Mini model (this may take a few minutes)
ollama pull phi3
```

### Step 7: Verify Ollama Setup

```bash
# Test that Ollama is working
ollama list

# You should see phi3 in the list
# Test the model
ollama run phi3 "Hello, how are you?"
```

### Step 8: Start the Application

```bash
# Make sure you're in the project directory and virtual environment is activated
cd /path/to/your/chatbot/project
source gpt-assistant-env/bin/activate  # On macOS/Linux

# Start the FastAPI server
uvicorn personal_assistant:app --reload --port 8001
```

### Step 9: Access the Application

1. **Backend API**: Open http://localhost:8001 in your browser
2. **API Documentation**: Visit http://localhost:8001/docs for Swagger UI
3. **Frontend**: Open the `frontend.html` file in your web browser

## Project Structure

```
chatbot/
├── personal_assistant.py      # Main FastAPI backend
├── frontend.html             # Web interface
├── user_data.json           # User data storage
├── gpt-assistant-env/       # Python virtual environment
├── PROJECT_REPORT.md        # Detailed project documentation
├── UI_TEST_QUERIES.md       # Test queries for demonstration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Quick Start Commands

```bash
# 1. Set up environment
python3 -m venv gpt-assistant-env
source gpt-assistant-env/bin/activate

# 2. Install dependencies
pip install fastapi uvicorn openai

# 3. Install and setup Ollama
brew install ollama  # macOS
ollama serve
ollama pull phi3

# 4. Start application
uvicorn personal_assistant:app --reload --port 8001
```
## Usage

The assistant supports natural language commands for managing your personal data. Here are some examples:

- **Tasks**: "add task to buy groceries", "completed shopping"
- **Contacts**: "add Johns phone 0771234567", "show all contacts"
- **Expenses**: "spent 25 on lunch", "record expense 100 for groceries"
- **Goals**: "add goal to learn Spanish", "set goal exercise daily"
- **Reminders**: "remind me to call mom", "add reminder pay rent"
- **Notes**: "note that meeting went well", "add note project deadline"
- **Schedule**: "schedule meeting tomorrow", "book appointment on 2025-07-15"

For comprehensive testing queries and examples, see `UI_TEST_QUERIES.md`.

## API Endpoints

### Main Chat Endpoint
- **POST** `/chat`
  - Body: `{"prompt": "your natural language query"}`
  - Returns: `{"response": "assistant response"}`

### Example API Usage
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "add task to buy groceries"}'
```

## Configuration

### Changing AI Model
To use a different Ollama model, modify the `personal_assistant.py` file:

```python
# In the chat endpoint, change the model name
response = client.chat.completions.create(
    model="llama2",  # or any other Ollama model
    messages=[...]
)
```

### Changing Server Port
```bash
uvicorn personal_assistant:app --reload --port 8080
```

### Data Storage
User data is stored in `user_data.json`. To reset all data, simply delete this file and restart the application.

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'fastapi'"
**Solution**: Make sure virtual environment is activated and packages are installed
```bash
source gpt-assistant-env/bin/activate
pip install fastapi uvicorn openai
```

#### 2. "Connection refused" when calling AI
**Solution**: Ensure Ollama service is running
```bash
ollama serve
```

#### 3. "Model not found" error
**Solution**: Download the Phi-3 model
```bash
ollama pull phi3
```

#### 4. Port already in use
**Solution**: Use a different port
```bash
uvicorn personal_assistant:app --reload --port 8002
```

#### 5. Frontend can't connect to backend
**Solution**: Update the frontend.html file with the correct backend URL if you changed the port

### Checking System Status

```bash
# Check if virtual environment is active
which python

# Check installed packages
pip list

# Check Ollama status
ollama list

# Test backend
curl http://localhost:8001/chat -X POST -H "Content-Type: application/json" -d '{"prompt": "hello"}'
```

## Development

### Adding New Natural Language Patterns

Edit `personal_assistant.py` and add new regex patterns:

```python
# Example: Adding new task patterns
task_patterns = [
    r'(?:add|create|new)\s+(?:task|todo)\s+to\s+(.+)',
    r'your_new_pattern_here',  # Add your pattern
]
```

### Adding New Data Categories

1. Add to the data structure in `personal_assistant.py`
2. Create validation functions
3. Add regex patterns for natural language processing
4. Update the frontend interface

### Testing

Use the queries in `UI_TEST_QUERIES.md` to test functionality:

```bash
# Test adding valid data
curl -X POST http://localhost:8001/chat -H "Content-Type: application/json" -d '{"prompt": "add task study for exam"}'

# Test validation (should fail)
curl -X POST http://localhost:8001/chat -H "Content-Type: application/json" -d '{"prompt": "add task a"}'
```

## Security Considerations

- All data is stored locally in JSON files
- No external API calls (except to local Ollama)
- No user authentication (single-user system)
- For production use, consider adding authentication and database storage

## Performance

- **Response Time**: < 100ms for pattern-matched queries
- **AI Response**: < 2s for LLM-processed queries
- **Memory Usage**: ~1GB RAM (including AI model)
- **Storage**: Minimal (JSON files)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly using the provided test queries
5. Submit a pull request

## License

This project is open source. Feel free to use, modify, and distribute as needed.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the `PROJECT_REPORT.md` for technical details
3. Test with queries from `UI_TEST_QUERIES.md`

---

**Happy chatting with your AI assistant!** 🤖✨
