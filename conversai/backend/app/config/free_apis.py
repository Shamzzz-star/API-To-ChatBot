"""
Pre-configured free APIs for ConversAI
All these APIs are FREE to use!
"""

FREE_APIS = [
    {
        "api_id": "weather-openweather",
        "api_name": "OpenWeatherMap",
        "description": "Get current weather information for any city",
        "intent_keywords": ["weather", "temperature", "forecast", "rain", "sunny", "climate"],
        "category": "weather",
        "endpoint": "https://api.openweathermap.org/data/2.5/weather",
        "method": "GET",
        "auth_config": {
            "type": "api_key",
            "param_name": "appid",
            "param_location": "query"  # or "header"
        },
        "parameters": {
            "required": [
                {
                    "name": "q",
                    "type": "string",
                    "description": "City name",
                    "llm_extraction_hint": "Extract city/location from query"
                }
            ],
            "optional": [
                {
                    "name": "units",
                    "type": "string",
                    "default": "metric",
                    "allowed_values": ["metric", "imperial", "standard"]
                }
            ]
        },
        "response_mapping": {
            "temperature": "main.temp",
            "feels_like": "main.feels_like",
            "condition": "weather[0].description",
            "humidity": "main.humidity",
            "wind_speed": "wind.speed",
            "city": "name",
            "country": "sys.country"
        },
        "response_template": "The weather in {city}, {country} is {condition} with a temperature of {temperature}°C (feels like {feels_like}°C). Humidity is {humidity}%.",
        "rate_limit": {
            "requests_per_minute": 60,
            "requests_per_day": 1000
        },
        "is_system": True,
        "is_active": True
    },
    {
        "api_id": "crypto-coingecko",
        "api_name": "CoinGecko",
        "description": "Get cryptocurrency prices and market data",
        "intent_keywords": ["crypto", "cryptocurrency", "bitcoin", "ethereum", "btc", "eth", "price", "coin"],
        "category": "cryptocurrency",
        "endpoint": "https://api.coingecko.com/api/v3/simple/price",
        "method": "GET",
        "auth_config": {
            "type": "none"
        },
        "parameters": {
            "required": [
                {
                    "name": "ids",
                    "type": "string",
                    "description": "Cryptocurrency ID (bitcoin, ethereum, etc)",
                    "llm_extraction_hint": "Extract cryptocurrency name from query"
                }
            ],
            "optional": [
                {
                    "name": "vs_currencies",
                    "type": "string",
                    "default": "usd",
                    "allowed_values": ["usd", "eur", "gbp", "jpy", "inr"]
                },
                {
                    "name": "include_24hr_change",
                    "type": "boolean",
                    "default": "true"
                }
            ]
        },
        "response_mapping": None,  # Dynamic response, handled by category formatter
        "response_template": None,  # Use category-based formatting
        "rate_limit": {
            "requests_per_minute": 50
        },
        "is_system": True,
        "is_active": True
    },
    {
        "api_id": "news-newsapi",
        "api_name": "NewsAPI",
        "description": "Get latest news articles and headlines",
        "intent_keywords": ["news", "article", "headline", "latest", "current events"],
        "category": "news",
        "endpoint": "https://newsapi.org/v2/everything",
        "method": "GET",
        "auth_config": {
            "type": "api_key",
            "param_name": "apiKey",
            "param_location": "query"
        },
        "parameters": {
            "required": [
                {
                    "name": "q",
                    "type": "string",
                    "description": "Search keyword or phrase",
                    "llm_extraction_hint": "Extract news topic from query"
                }
            ],
            "optional": [
                {
                    "name": "pageSize",
                    "type": "integer",
                    "default": "5"
                },
                {
                    "name": "sortBy",
                    "type": "string",
                    "default": "publishedAt",
                    "allowed_values": ["publishedAt", "relevancy", "popularity"]
                }
            ]
        },
        "response_mapping": {
            "articles": "articles"
        },
        "response_template": "Here are the latest news on {topic}:\n{articles}",
        "rate_limit": {
            "requests_per_day": 100
        },
        "is_system": True,
        "is_active": True
    },
    {
        "api_id": "dictionary-free",
        "api_name": "Free Dictionary API",
        "description": "Get word definitions, phonetics, and examples",
        "intent_keywords": ["define", "definition", "meaning", "what is", "dictionary"],
        "category": "dictionary",
        "endpoint": "https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
        "method": "GET",
        "auth_config": {
            "type": "none"
        },
        "parameters": {
            "required": [
                {
                    "name": "word",
                    "type": "string",
                    "description": "Word to define",
                    "llm_extraction_hint": "Extract word to define",
                    "in_path": True
                }
            ]
        },
        "response_mapping": {
            "word": "data[0].word",
            "phonetic": "data[0].phonetic",
            "definition": "data[0].meanings[0].definitions[0].definition",
            "example": "data[0].meanings[0].definitions[0].example",
            "part_of_speech": "data[0].meanings[0].partOfSpeech"
        },
        "response_template": "{word} ({phonetic}): {definition}. Example: {example}",
        "rate_limit": {
            "requests_per_minute": 100
        },
        "is_system": True,
        "is_active": True
    },
    {
        "api_id": "exchange-rates",
        "api_name": "Exchange Rates API",
        "description": "Get currency exchange rates",
        "intent_keywords": ["exchange", "currency", "convert", "rate", "usd", "eur"],
        "category": "finance",
        "endpoint": "https://api.exchangerate-api.com/v4/latest/{base}",
        "method": "GET",
        "auth_config": {
            "type": "none"
        },
        "parameters": {
            "required": [
                {
                    "name": "base",
                    "type": "string",
                    "description": "Base currency code (USD, EUR, etc)",
                    "llm_extraction_hint": "Extract base currency",
                    "in_path": True,
                    "default": "USD"
                }
            ]
        },
        "response_mapping": {
            "base": "base",
            "rates": "rates",
            "date": "date"
        },
        "response_template": "Exchange rates for {base}: {rates}",
        "rate_limit": {
            "requests_per_hour": 1500
        },
        "is_system": True,
        "is_active": True
    },
    {
        "api_id": "facts-ninja",
        "api_name": "API Ninjas Facts",
        "description": "Get random interesting facts",
        "intent_keywords": ["fact", "facts", "random fact", "tell me", "interesting"],
        "category": "entertainment",
        "endpoint": "https://api.api-ninjas.com/v1/facts",
        "method": "GET",
        "auth_config": {
            "type": "api_key",
            "param_name": "X-Api-Key",
            "param_location": "header"
        },
        "parameters": {
            "optional": [
                {
                    "name": "limit",
                    "type": "integer",
                    "default": "1"
                }
            ]
        },
        "response_mapping": {
            "fact": "[0].fact"
        },
        "response_template": "Here's an interesting fact: {fact}",
        "rate_limit": {
            "requests_per_month": 50000
        },
        "is_system": True,
        "is_active": True
    },
    {
        "api_id": "wikipedia-api",
        "api_name": "Wikipedia API",
        "description": "Search Wikipedia for information",
        "intent_keywords": ["wikipedia", "wiki", "information about", "tell me about"],
        "category": "knowledge",
        "endpoint": "https://en.wikipedia.org/api/rest_v1/page/summary/{title}",
        "method": "GET",
        "auth_config": {
            "type": "none"
        },
        "parameters": {
            "required": [
                {
                    "name": "title",
                    "type": "string",
                    "description": "Wikipedia article title",
                    "llm_extraction_hint": "Extract topic to search",
                    "in_path": True
                }
            ]
        },
        "response_mapping": {
            "title": "title",
            "extract": "extract",
            "url": "content_urls.desktop.page"
        },
        "response_template": "{title}: {extract}\n\nRead more: {url}",
        "rate_limit": {
            "requests_per_second": 200
        },
        "is_system": True,
        "is_active": True
    },
    {
        "api_id": "github-api",
        "api_name": "GitHub Repository API",
        "description": "Get information about GitHub repositories",
        "intent_keywords": ["github", "repository", "repo", "project", "code"],
        "category": "development",
        "endpoint": "https://api.github.com/repos/{owner}/{repo}",
        "method": "GET",
        "auth_config": {
            "type": "none"
        },
        "parameters": {
            "required": [
                {
                    "name": "owner",
                    "type": "string",
                    "description": "Repository owner username",
                    "llm_extraction_hint": "Extract owner from query",
                    "in_path": True
                },
                {
                    "name": "repo",
                    "type": "string",
                    "description": "Repository name",
                    "llm_extraction_hint": "Extract repo name from query",
                    "in_path": True
                }
            ]
        },
        "response_mapping": {
            "name": "name",
            "description": "description",
            "stars": "stargazers_count",
            "language": "language",
            "url": "html_url"
        },
        "response_template": "{name}: {description}\nStars: {stars} | Language: {language}\n{url}",
        "rate_limit": {
            "requests_per_hour": 60
        },
        "is_system": True,
        "is_active": True
    }
]
