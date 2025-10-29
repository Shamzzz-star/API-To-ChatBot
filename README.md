# ConversAI

> An LLM-powered conversational platform that interprets natural language queries, automatically selects and invokes the right APIs, and returns human-like responses.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat&logo=react)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Overview

ConversAI bridges the gap between human language and REST APIs. Users ask questions in plain English — the system classifies intent, extracts entities (dates, locations, teams), maps parameters, invokes APIs securely, and formats responses naturally using an LLM.

**Example Queries:**
- "What's the weather in London tomorrow?" → Calls weather API with location + date
- "Bitcoin price" → Fetches real-time crypto data
- "Liverpool's last match result" → Queries sports API for team fixtures
- "Define serendipity" → Returns dictionary definition

---

## Key Features

- **Natural Language Processing**: Intent classification, entity extraction, and context awareness
- **8+ Pre-Configured APIs**: Weather, news, cryptocurrency, sports, dictionary, and more
- **Custom API Integration**: Add, edit, and delete user-defined APIs with full CRUD operations
- **LLM-Powered Responses**: Natural formatting with conversational error messages
- **Security**: AES-256 encrypted API keys, JWT authentication, CORS protection
- **Performance**: Response caching, rate limiting, auto-retry logic

---

## Tech Stack

**Backend:** FastAPI, Python 3.11+, SQLAlchemy, Groq API (Llama 3.1)  
**Frontend:** React 18, Vite, Tailwind CSS, Zustand  
**Database:** SQLite (dev) / PostgreSQL (prod)  
**DevOps:** Docker, Docker Compose, Uvicorn

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Groq API Key ([Get free tier](https://console.groq.com))

### Installation

```bash
# Clone repository
git clone https://github.com/Shamzzz-star/API-To-ChatBot.git
cd conversai

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add GROQ_API_KEY and ENCRYPTION_KEY

# Frontend setup
cd ../frontend
npm install

# Run application
# Terminal 1 (Backend):
cd backend
uvicorn app.main:app --reload

# Terminal 2 (Frontend):
cd frontend
npm run dev
```

**Access:** Frontend at http://localhost:3000 | API Docs at http://localhost:8000/docs

### Docker

```bash
docker-compose up --build
```

---

## Usage Examples

```
You: What's the weather in Tokyo?
Bot: The current weather in Tokyo is 18°C with clear skies. 
     Humidity is 65% and wind speed is 12 km/h.

You: Bitcoin price
Bot: Bitcoin is currently trading at $34,521.30 USD, 
     up 2.4% in the last 24 hours.

You: Weather in Paris yesterday
Bot: Yesterday in Paris it was 15°C with partly cloudy skies.
```

The system understands natural dates: "yesterday", "tomorrow", "last week", etc.

---

## Configuration

Create `.env` in `backend/` directory:

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here
ENCRYPTION_KEY=your-32-character-encryption-key

# Optional API Keys (free tier available)
OPENWEATHER_API_KEY=your_openweather_key
NEWSAPI_KEY=your_newsapi_key

# Database
DATABASE_URL=sqlite:///./conversai.db

# Security
JWT_SECRET_KEY=your-jwt-secret-key

# Server
HOST=0.0.0.0
PORT=8000
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed configuration options.

---

## Documentation

- **[API Documentation](API_DOCUMENTATION.md)** - Endpoints, request/response schemas
- **[Setup Guide](SETUP_GUIDE.md)** - Detailed installation, configuration, deployment

---

## Project Structure

```
conversai/
├── backend/
│   ├── app/
│   │   ├── api/              # API routes (chat, api_management)
│   │   ├── core/             # Config, database, security
│   │   ├── models/           # Database models
│   │   ├── services/         # Business logic (intent, entity, mapper)
│   │   └── main.py           # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── api/              # API client
│   │   └── App.jsx
│   └── package.json
└── docker-compose.yml
```

---

## Custom API Integration

1. Click "Add API" in the sidebar
2. Configure: name, base URL, endpoint, method, auth type
3. Define parameters and response mappings
4. Save and test

APIs can be edited or deleted via the UI. System APIs are read-only.

---

## Future Roadmap

- **Auto-Config from API Docs** (Q1 2026): Upload OpenAPI/Swagger specs for automatic configuration
- **Multi-Endpoint APIs**: Support complex APIs with multiple operations
- **API Marketplace**: Share and discover pre-configured APIs
- **Conversation Memory**: Context across sessions

---

## Contributing

Contributions welcome! Fork the repo, create a feature branch, and submit a PR.

**Guidelines:** Follow PEP 8 (Python), ESLint (JavaScript), write tests, update docs.

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Contact

**Developer**: [Shamzzz-star](https://github.com/Shamzzz-star)  
**Repository**: [API-To-ChatBot](https://github.com/Shamzzz-star/API-To-ChatBot)  
**Issues**: [Report a bug](https://github.com/Shamzzz-star/API-To-ChatBot/issues)

---

<div align="center">

**Star this repository if you find it helpful!**

</div>
