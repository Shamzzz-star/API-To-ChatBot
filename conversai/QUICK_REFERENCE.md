# 🚀 ConversAI - Quick Reference

## ⚡ Quick Start (3 Steps)

### 1. Backend (Terminal 1)
```powershell
cd "d:\SEM 3\GENAI\API\conversai\backend"
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```
**Running**: http://localhost:8000

### 2. Frontend (Terminal 2)
```powershell
cd "d:\SEM 3\GENAI\API\conversai\frontend"
npm run dev
```
**Running**: http://localhost:3000

### 3. Open Browser
Navigate to: **http://localhost:3000**

---

## 💬 Test Queries

Try these queries in the chat:

| Query | API Used | Expected Response |
|-------|----------|-------------------|
| "What's the weather in Paris?" | OpenWeatherMap | Current weather conditions |
| "Bitcoin price" | CoinGecko | Current BTC price in USD |
| "Latest AI news" | NewsAPI | Recent AI-related headlines |
| "Define quantum computing" | Free Dictionary API | Word definition |
| "USD to EUR rate" | ExchangeRate-API | Current exchange rate |
| "Random fact" | API Ninjas | Interesting random fact |
| "Who is Albert Einstein?" | Wikipedia | Brief biography |
| "Popular Python repos" | GitHub API | Trending Python repositories |

---

## 📂 Project Structure

```
conversai/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # REST endpoints
│   │   ├── core/           # Config, security, database
│   │   ├── models/         # SQLAlchemy models
│   │   ├── services/       # Business logic
│   │   ├── config/         # API configurations
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables
│
├── frontend/                # React Frontend
│   ├── src/
│   │   ├── api/           # Axios client
│   │   ├── components/    # React components
│   │   ├── store/         # Zustand state
│   │   ├── App.jsx        # Main app
│   │   └── main.jsx       # Entry point
│   ├── package.json       # npm dependencies
│   └── vite.config.js     # Vite config
│
├── docs/                   # Documentation
└── tests/                  # Test files
```

---

## 🔑 Important Files

### Backend Configuration
- **Environment**: `backend/.env`
- **API Keys**: Add your keys here
- **Main App**: `backend/app/main.py`

### Frontend Configuration
- **Environment**: `frontend/.env`
- **API Client**: `frontend/src/api/client.js`
- **State Management**: `frontend/src/store/chatStore.js`

### Pre-configured APIs
- **File**: `backend/app/config/free_apis.py`
- **Count**: 8 free APIs
- **Editable**: Add more APIs here

---

## 🛠️ Common Commands

### Backend
```powershell
# Start server
python -m uvicorn app.main:app --reload

# Install package
pip install package_name

# Run tests
pytest tests/ -v

# View logs
# Check terminal output
```

### Frontend
```powershell
# Start dev server
npm run dev

# Install package
npm install package_name

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🌐 Important URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Chat interface |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Swagger UI |
| ReDoc | http://localhost:8000/redoc | Alternative docs |
| Health Check | http://localhost:8000/health | Server status |

---

## 📋 API Endpoints

### Chat
- `POST /api/chat/message` - Send message
- `GET /api/chat/history/{session_id}` - Get history

### API Management
- `GET /api/apis/list` - List all APIs
- `POST /api/apis/register` - Register new API
- `POST /api/apis/{id}/test` - Test API

---

## 🐛 Troubleshooting

### Backend Won't Start
```powershell
# Check virtual environment
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt

# Check port 8000 is free
netstat -ano | findstr :8000
```

### Frontend Won't Start
```powershell
# Reinstall node_modules
Remove-Item -Recurse -Force node_modules
npm install

# Check port 3000 is free
netstat -ano | findstr :3000
```

### CORS Error
1. Check backend is running
2. Verify ALLOWED_ORIGINS in backend/.env
3. Restart backend server

### No Response from Chat
1. Check backend logs for errors
2. Verify GROQ_API_KEY in backend/.env
3. Check browser console (F12)
4. Test backend: http://localhost:8000/health

---

## 🔧 Configuration

### Backend Environment (.env)
```bash
# Required
GROQ_API_KEY=your_key_here

# Optional API Keys
OPENWEATHER_API_KEY=your_key
NEWSAPI_KEY=your_key
API_NINJAS_KEY=your_key
GITHUB_TOKEN=your_token

# Database
DATABASE_URL=sqlite:///./conversai.db

# Server
DEBUG=true
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend Environment (.env)
```bash
VITE_API_URL=http://localhost:8000
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `README.md` | Main project overview |
| `backend/README.md` | Backend documentation |
| `frontend/README.md` | Frontend documentation |
| `frontend/INSTALLATION.md` | Frontend setup guide |
| `docs/SETUP_GUIDE.md` | Complete setup instructions |
| `docs/API_EXAMPLES.md` | Usage examples |
| `docs/PROJECT_REPORT.md` | Academic report |
| `TASK_COMPLETION.md` | Requirements checklist |

---

## ✅ Current Status

### ✨ **BOTH SERVERS RUNNING**

- ✅ Backend: http://localhost:8000
- ✅ Frontend: http://localhost:3000
- ✅ 8 APIs configured
- ✅ Database initialized
- ✅ Chat interface ready

### 🎯 What Works

- ✅ Send messages in natural language
- ✅ Get responses from 8 different APIs
- ✅ View conversation history
- ✅ See API usage metadata
- ✅ Browse registered APIs in sidebar
- ✅ Responsive design on all devices
- ✅ Error handling and retry logic
- ✅ Response caching

---

## 🎨 UI Features

### Chat Interface
- Message bubbles (blue for user, white for AI)
- Typing indicator with animated dots
- Auto-scroll to latest message
- Message timestamps
- API metadata (which API used, cached status)
- Character counter (max 1000)

### API Sidebar
- View all 8 registered APIs
- Category badges with colors
- Active/inactive status indicators
- Intent keywords for each API
- Slide-in animation from right
- Mobile-responsive overlay

### Input Controls
- Multi-line text input
- Enter to send, Shift+Enter for new line
- Send button with loading state
- Disabled while processing
- Clear visual feedback

---

## 🔄 Workflow

### Typical User Flow:
1. User types query in chat input
2. Frontend sends to `/api/chat/message`
3. Backend extracts intent with LLM
4. Backend selects appropriate API
5. Backend calls external API (or uses cache)
6. Backend formats response naturally
7. Frontend displays response with metadata
8. Conversation saved to database

### Response Time:
- **Cached**: < 100ms
- **LLM + API**: 1-2 seconds
- **With retry**: up to 3 seconds

---

## 💡 Tips & Tricks

### Testing
1. Start with simple queries: "weather in Paris"
2. Try follow-up questions: "what about London?"
3. Test error handling: "weather in InvalidCity"
4. Check caching: repeat same query twice

### Development
1. Keep both terminals open (backend + frontend)
2. Watch logs for errors
3. Use browser DevTools (F12) to debug
4. Test API docs at /docs endpoint

### Performance
1. Responses are cached (900s TTL)
2. First query to an API may be slower
3. Subsequent queries use cache (faster)
4. Clear cache by restarting backend

---

## 🎓 For Submission

### What to Include:
1. **Code**: Full repository
2. **Documentation**: All 8+ docs
3. **Demo**: Screenshots or video
4. **Report**: `docs/PROJECT_REPORT.md`

### Demo Script:
1. Show chat interface
2. Send weather query
3. Show response with metadata
4. Open API sidebar
5. Show different API categories
6. Send crypto query
7. Show news query
8. Highlight features (typing indicator, caching, etc.)

---

## 🚀 Next Steps

### If Adding Custom APIs:
1. Open backend: `app/config/free_apis.py`
2. Add new API configuration
3. Restart backend server
4. Test in chat interface

### If Customizing UI:
1. Edit: `frontend/src/components/`
2. Change colors: `frontend/tailwind.config.js`
3. Vite auto-reloads changes

### If Deploying:
1. Use Docker: `docker-compose up`
2. Or deploy separately to cloud
3. Update CORS origins
4. Set production environment variables

---

## 📞 Support

### Check These First:
1. Both servers running?
2. Environment variables set?
3. Dependencies installed?
4. Ports 3000 and 8000 free?

### Common Fixes:
- Restart both servers
- Clear browser cache
- Reinstall dependencies
- Check .env files

---

## 🎉 Success Indicators

You're all set if you see:
- ✅ Welcome screen on http://localhost:3000
- ✅ Can send messages and get responses
- ✅ API metadata shows below messages
- ✅ Sidebar opens with 8 APIs listed
- ✅ No errors in browser console
- ✅ Backend logs show successful requests

---

**Everything is working! Start chatting with your APIs!** 🎊

Open http://localhost:3000 and try: **"What's the weather in Paris?"**
