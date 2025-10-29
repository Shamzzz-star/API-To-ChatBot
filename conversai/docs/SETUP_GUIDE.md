# 🚀 Step-by-Step Setup Guide for ConversAI

This guide will walk you through setting up ConversAI from scratch, even if you're new to Python or web development.

## 📋 Prerequisites Checklist

Before you start, make sure you have:

- [ ] Python 3.11 or higher installed
- [ ] pip (Python package manager)
- [ ] A text editor (VS Code, Notepad++, etc.)
- [ ] Internet connection
- [ ] 10-15 minutes of time

## 🎯 Step 1: Get Your Free Groq API Key

**Groq provides FREE access to powerful LLM models!**

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account (you can use Google/GitHub)
3. Navigate to API Keys section
4. Click "Create API Key"
5. Copy your API key (format: `gsk_...`)
6. **Keep it safe!** You'll need it in Step 4

**Free Tier Limits:** 14,400 requests per day (more than enough for development!)

## 🎯 Step 2: Download or Clone ConversAI

### Option A: Using Git
```bash
git clone <repository-url>
cd conversai
```

### Option B: Download ZIP
1. Download the project ZIP file
2. Extract it to a folder
3. Open terminal/command prompt in that folder

## 🎯 Step 3: Set Up Python Environment

### Windows:
```powershell
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Your prompt should now show (venv)

# Install dependencies
pip install -r requirements.txt
```

### Mac/Linux:
```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Your prompt should now show (venv)

# Install dependencies
pip install -r requirements.txt
```

**This step installs:**
- FastAPI (web framework)
- Groq client (for LLM)
- SQLAlchemy (database)
- And other dependencies

**Expected time:** 2-3 minutes

## 🎯 Step 4: Configure Environment Variables

1. **Navigate to project root** (one folder up from backend):
   ```bash
   cd ..
   ```

2. **Copy the example environment file**:
   ```powershell
   # Windows
   copy .env.example .env
   
   # Mac/Linux
   cp .env.example .env
   ```

3. **Edit `.env` file** with your text editor:
   
   Find this line:
   ```
   GROQ_API_KEY=your-groq-api-key-here
   ```
   
   Replace with your actual Groq API key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here_from_step_1
   ```

4. **Optional:** Add other free API keys (for full functionality):

   **OpenWeatherMap** (for weather queries):
   - Visit: [openweathermap.org/api](https://openweathermap.org/api)
   - Sign up for free account
   - Get API key
   - Add to `.env`:
     ```
     OPENWEATHER_API_KEY=your_key_here
     ```

   **NewsAPI** (for news queries):
   - Visit: [newsapi.org](https://newsapi.org)
   - Sign up for free developer account
   - Get API key
   - Add to `.env`:
     ```
     NEWSAPI_KEY=your_key_here
     ```

   **Don't worry!** Many APIs work without keys (cryptocurrency, dictionary, exchange rates, etc.)

## 🎯 Step 5: Run the Backend Server

```bash
# Make sure you're in the backend folder and venv is activated
cd backend

# Windows
uvicorn app.main:app --reload

# Mac/Linux
uvicorn app.main:app --reload
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
Starting ConversAI...
✅ Loaded 8 system APIs
✅ ConversAI is ready!
INFO:     Application startup complete.
```

🎉 **Success!** Your backend is now running!

## 🎯 Step 6: Test the API

### Option 1: Using Your Browser

1. Open your browser
2. Go to: [http://localhost:8000/docs](http://localhost:8000/docs)
3. You'll see the **Swagger UI** with all API endpoints
4. Click on **POST /api/chat/message**
5. Click **"Try it out"**
6. Enter test message:
   ```json
   {
     "message": "What is Bitcoin's price?"
   }
   ```
7. Click **Execute**
8. See the response! 🎉

### Option 2: Using PowerShell (Windows)

```powershell
# Test basic endpoint
Invoke-WebRequest -Uri http://localhost:8000/health

# Send a chat message
$body = @{
    message = "What is the weather in New York?"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/api/chat/message -Method POST -Body $body -ContentType "application/json"
```

### Option 3: Using curl (Mac/Linux/Windows Git Bash)

```bash
# Test health endpoint
curl http://localhost:8000/health

# Send a chat message
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the price of Bitcoin?"}'
```

## 🎯 Step 7: Try Different Queries

Now that it's working, try these example queries:

```bash
# Cryptocurrency price
{"message": "What is Ethereum's current price?"}

# Dictionary definition
{"message": "Define artificial intelligence"}

# Currency exchange
{"message": "Convert 100 USD to EUR"}

# Random fact
{"message": "Tell me an interesting fact"}

# Wikipedia
{"message": "Tell me about Python programming"}

# Multiple intents
{"message": "What's the weather in London and price of Bitcoin?"}
```

## 🎯 Step 8: View Available APIs

List all pre-configured APIs:

```bash
curl http://localhost:8000/api/apis/list
```

You should see 8 system APIs ready to use!

## 🎯 Step 9: (Optional) Use Docker

If you prefer Docker:

```bash
# Make sure Docker is installed and running

# From project root
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

## 📊 Verification Checklist

Make sure everything works:

- [ ] Server starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Health check returns {"status": "healthy"}
- [ ] Can send a chat message and get response
- [ ] Intent is correctly detected
- [ ] Response is in natural language

## 🐛 Troubleshooting

### Problem: "python: command not found"
**Solution:** Install Python 3.11+ from [python.org](https://python.org)

### Problem: "GROQ_API_KEY not set"
**Solution:** 
1. Check that `.env` file exists in project root
2. Verify GROQ_API_KEY is set correctly (no quotes, no spaces)
3. Restart the server

### Problem: "Module not found" errors
**Solution:**
```bash
# Make sure virtual environment is activated
# Then reinstall:
pip install --upgrade -r requirements.txt
```

### Problem: Port 8000 already in use
**Solution:**
```bash
# Use a different port:
uvicorn app.main:app --reload --port 8001
```

### Problem: Database errors
**Solution:**
```bash
# Delete the database file and restart:
rm conversai.db  # Mac/Linux
del conversai.db  # Windows
```

### Problem: API returns errors
**Solution:**
1. Check your API keys are valid
2. Check your internet connection
3. Some APIs have rate limits - wait a moment and try again

## 🎓 Next Steps

Now that ConversAI is running:

1. **Explore the API docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
2. **Read the main README**: Learn about features and architecture
3. **Try custom API registration**: Add your own APIs
4. **Build a frontend**: Create a UI for the chatbot
5. **Customize**: Modify prompts, add new APIs, improve responses

## 📚 Additional Resources

- **Groq Documentation**: [console.groq.com/docs](https://console.groq.com/docs)
- **FastAPI Tutorial**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Free API List**: [github.com/public-apis/public-apis](https://github.com/public-apis/public-apis)

## 💡 Tips for Success

1. **Start Simple**: Test with basic queries first
2. **Check Logs**: Read the console output for debugging
3. **Use Swagger UI**: Best way to test endpoints interactively
4. **Cache Works**: Second identical query will be much faster
5. **Context Matters**: Use same session_id for conversation context

## ✅ You're All Set!

Congratulations! You now have a fully functional AI chatbot that can interact with multiple APIs using natural language. 🎉

**Questions?** Create an issue on GitHub or check the troubleshooting section.

**Happy Coding!** 🚀
