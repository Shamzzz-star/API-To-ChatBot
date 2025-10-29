# ConversAI Backend

This is the backend API for ConversAI - A natural language chatbot for seamless API interaction.

## Features

- 🤖 Natural language processing using Groq's free LLM API
- 🔌 8+ pre-configured free APIs (Weather, Crypto, News, Dictionary, etc.)
- ⚡ Fast response with in-memory caching
- 🔒 Secure API key encryption
- 📊 Conversation history management
- 🎨 Custom API registration system

## Quick Start

### Prerequisites

- Python 3.11+
- Groq API key (free from https://console.groq.com)

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Create `.env` file**:
```bash
cp ../.env.example .env
```

3. **Add your Groq API key** to `.env`:
```
GROQ_API_KEY=your-groq-api-key-here
```

4. **Optional**: Add other API keys for specific services:
```
OPENWEATHER_API_KEY=your-key (get from https://openweathermap.org/api)
NEWSAPI_KEY=your-key (get from https://newsapi.org)
```

5. **Run the server**:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Chat Endpoints

- `POST /api/chat/message` - Send a message and get AI response
- `GET /api/chat/history/{session_id}` - Get conversation history
- `POST /api/chat/session/new` - Create new conversation session
- `DELETE /api/chat/session/{session_id}` - End conversation

### API Management Endpoints

- `GET /api/apis/list` - List all available APIs
- `GET /api/apis/{api_id}` - Get API details
- `POST /api/apis/register` - Register custom API
- `PUT /api/apis/{api_id}` - Update API configuration
- `DELETE /api/apis/{api_id}` - Delete custom API
- `POST /api/apis/{api_id}/test` - Test API with sample data

## Example Usage

### Send a chat message:

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather in London?"}'
```

### List available APIs:

```bash
curl http://localhost:8000/api/apis/list
```

## Pre-configured Free APIs

1. **OpenWeatherMap** - Weather data (requires free API key)
2. **CoinGecko** - Cryptocurrency prices (no key required)
3. **NewsAPI** - News articles (requires free API key)
4. **Free Dictionary API** - Word definitions (no key required)
5. **Exchange Rates API** - Currency exchange (no key required)
6. **API Ninjas** - Random facts (requires free API key)
7. **Wikipedia API** - Wikipedia information (no key required)
8. **GitHub API** - Repository information (no key required)

## Database

By default, ConversAI uses SQLite for simplicity. The database file `conversai.db` will be created automatically in the project root.

For production, you can switch to PostgreSQL by updating `DATABASE_URL` in `.env`:

```
DATABASE_URL=postgresql://user:password@localhost:5432/conversai
```

## Testing

Run tests with pytest:

```bash
pytest tests/
```

## Project Structure

```
backend/
├── app/
│   ├── api/                 # API endpoints
│   │   ├── chat.py         # Chat endpoints
│   │   ├── api_management.py # API management
│   │   └── schemas.py      # Pydantic schemas
│   ├── core/               # Core functionality
│   │   ├── config.py       # Configuration
│   │   ├── security.py     # Security utilities
│   │   └── database.py     # Database connection
│   ├── models/             # Database models
│   │   └── database.py     # SQLAlchemy models
│   ├── services/           # Business logic
│   │   ├── llm_service.py  # LLM integration
│   │   ├── query_processor.py # Query processing
│   │   ├── api_mapper.py   # API mapping
│   │   ├── api_handler.py  # API requests
│   │   └── response_formatter.py # Response formatting
│   ├── config/             # Configuration files
│   │   └── free_apis.py    # Pre-configured APIs
│   └── main.py             # FastAPI application
├── requirements.txt        # Python dependencies
└── Dockerfile             # Docker configuration
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License
