# API Documentation

Complete reference for ConversAI REST API endpoints.

---

## Base URL

**Development:** `http://localhost:8000`  
**Production:** `https://your-domain.com`

---

## Authentication

Currently, the API does not require authentication for chat endpoints. Future versions will implement JWT-based authentication.

**Headers:**
```
Content-Type: application/json
```

---

## Endpoints

### 1. Chat Endpoint

Send a natural language query and receive a formatted response.

**Endpoint:** `POST /api/chat`

**Request Body:**
```json
{
  "message": "string (required)",
  "conversation_id": "string (optional, UUID format)"
}
```

**Response:**
```json
{
  "response": "string - Formatted natural language response",
  "api_used": "string - Name of the API that was called",
  "conversation_id": "string - UUID for conversation tracking",
  "cached": "boolean - Whether response was served from cache"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the weather in London?",
    "conversation_id": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

**Example Response:**
```json
{
  "response": "The current weather in London is 12°C with light rain. Humidity is 78% and wind speed is 15 km/h.",
  "api_used": "OpenWeather",
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "cached": false
}
```

**Status Codes:**
- `200 OK` - Successful response
- `400 Bad Request` - Invalid request format
- `500 Internal Server Error` - Server error or API call failed

---

### 2. List APIs

Retrieve all registered APIs (system and custom).

**Endpoint:** `GET /api/apis`

**Response:**
```json
[
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "base_url": "string",
    "endpoint": "string",
    "method": "string",
    "auth_type": "string",
    "keywords": ["array of strings"],
    "is_system": "boolean",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/apis
```

**Example Response:**
```json
[
  {
    "id": 1,
    "name": "OpenWeather",
    "description": "Get current weather and forecasts",
    "base_url": "https://api.openweathermap.org/data/2.5",
    "endpoint": "/weather",
    "method": "GET",
    "auth_type": "query",
    "keywords": ["weather", "forecast", "temperature", "climate"],
    "is_system": true,
    "created_at": "2025-01-15T10:00:00",
    "updated_at": "2025-01-15T10:00:00"
  },
  {
    "id": 10,
    "name": "GitHub Repos",
    "description": "Search GitHub repositories",
    "base_url": "https://api.github.com",
    "endpoint": "/search/repositories",
    "method": "GET",
    "auth_type": "header",
    "keywords": ["github", "repository", "repo", "code"],
    "is_system": false,
    "created_at": "2025-10-28T14:30:00",
    "updated_at": "2025-10-29T09:15:00"
  }
]
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Database error

---

### 3. Add Custom API

Register a new custom API configuration.

**Endpoint:** `POST /api/apis`

**Request Body:**
```json
{
  "name": "string (required)",
  "description": "string (required)",
  "base_url": "string (required, valid URL)",
  "endpoint": "string (required)",
  "method": "string (required, GET/POST/PUT/DELETE)",
  "auth_type": "string (required, none/query/header/bearer)",
  "auth_key_name": "string (optional)",
  "requires_api_key": "boolean (optional, default: false)",
  "keywords": ["array of strings (required)"],
  "parameters": "object (optional)",
  "response_mapping": "object (optional)",
  "example_response": "object (optional)",
  "rate_limit": "integer (optional)"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/apis \
  -H "Content-Type: application/json" \
  -d '{
    "name": "GitHub Repos",
    "description": "Search GitHub repositories",
    "base_url": "https://api.github.com",
    "endpoint": "/search/repositories",
    "method": "GET",
    "auth_type": "header",
    "auth_key_name": "Authorization",
    "requires_api_key": true,
    "keywords": ["github", "repository", "repo", "code"],
    "parameters": {
      "q": {
        "required": true,
        "type": "string",
        "description": "Search query"
      },
      "sort": {
        "required": false,
        "type": "string",
        "default": "stars"
      }
    },
    "response_mapping": {
      "items": "items",
      "name": "items[0].name",
      "stars": "items[0].stargazers_count"
    },
    "rate_limit": 60
  }'
```

**Example Response:**
```json
{
  "id": 10,
  "name": "GitHub Repos",
  "description": "Search GitHub repositories",
  "message": "API registered successfully"
}
```

**Status Codes:**
- `201 Created` - API successfully registered
- `400 Bad Request` - Invalid data or duplicate name
- `500 Internal Server Error` - Database error

---

### 4. Update Custom API

Update an existing custom API configuration.

**Endpoint:** `PUT /api/apis/{api_id}`

**Path Parameters:**
- `api_id` (integer, required) - ID of the API to update

**Request Body:** Same as Add Custom API (all fields optional)

**Example Request:**
```bash
curl -X PUT http://localhost:8000/api/apis/10 \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description for GitHub repository search",
    "keywords": ["github", "repository", "repo", "code", "search"]
  }'
```

**Example Response:**
```json
{
  "id": 10,
  "name": "GitHub Repos",
  "description": "Updated description for GitHub repository search",
  "message": "API updated successfully"
}
```

**Status Codes:**
- `200 OK` - API updated successfully
- `400 Bad Request` - Cannot update system API
- `404 Not Found` - API not found
- `500 Internal Server Error` - Database error

---

### 5. Delete Custom API

Remove a custom API configuration.

**Endpoint:** `DELETE /api/apis/{api_id}`

**Path Parameters:**
- `api_id` (integer, required) - ID of the API to delete

**Example Request:**
```bash
curl -X DELETE http://localhost:8000/api/apis/10
```

**Example Response:**
```json
{
  "message": "API deleted successfully"
}
```

**Status Codes:**
- `200 OK` - API deleted successfully
- `400 Bad Request` - Cannot delete system API
- `404 Not Found` - API not found
- `500 Internal Server Error` - Database error

---

### 6. Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /health`

**Example Request:**
```bash
curl -X GET http://localhost:8000/health
```

**Example Response:**
```json
{
  "status": "healthy",
  "environment": "development"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

### 7. API Information

Get information about the ConversAI API.

**Endpoint:** `GET /api/info`

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/info
```

**Example Response:**
```json
{
  "name": "ConversAI",
  "version": "1.0.0",
  "llm_model": "llama-3.1-8b-instant",
  "features": [
    "Natural language API interaction",
    "8+ pre-configured free APIs",
    "Custom API registration",
    "Conversation context management",
    "Response caching",
    "Intent classification"
  ]
}
```

**Status Codes:**
- `200 OK` - Success

---

## Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": "string - Error message description"
}
```

**Common Error Status Codes:**
- `400 Bad Request` - Invalid input or request format
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server-side error

---

## Rate Limiting

Default rate limits (configurable via environment variables):

- **60 requests per minute** per IP
- **1000 requests per day** per IP

When rate limit is exceeded:

**Status Code:** `429 Too Many Requests`

**Response:**
```json
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

---

## Caching

Responses are cached based on API type:

| API Type | Cache Duration |
|----------|----------------|
| Weather | 10 minutes |
| Crypto | 1 minute |
| News | 30 minutes |
| Other | 5 minutes |

Cached responses include `"cached": true` in the response body.

---

## Interactive Documentation

Visit the following URLs when running the application:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

These provide interactive API testing and complete schema documentation.

---

## Webhooks (Future)

Planned feature for subscribing to API events and updates.

**Coming in Q2 2026.**

---

## Support

For issues or questions:

- **GitHub Issues:** [Report a bug](https://github.com/Shamzzz-star/API-To-ChatBot/issues)
- **Documentation:** [README](README.md)
- **Setup Guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
