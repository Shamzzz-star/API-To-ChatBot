# 📝 API Examples and Use Cases

This document provides comprehensive examples of how to use ConversAI for various tasks.

## 🌟 Basic Examples

### 1. Weather Queries

**Simple query:**
```json
{
  "message": "What's the weather in London?"
}
```

**With follow-up (using same session_id):**
```json
{
  "message": "How about Paris?",
  "session_id": "abc-123-def"
}
```

**Multiple cities:**
```json
{
  "message": "Compare weather in Tokyo and Sydney"
}
```

### 2. Cryptocurrency Prices

**Single coin:**
```json
{
  "message": "What is the current price of Bitcoin?"
}
```

**Multiple coins:**
```json
{
  "message": "Show me prices for Bitcoin and Ethereum"
}
```

**Casual language:**
```json
{
  "message": "How much is BTC worth?"
}
```

### 3. News Queries

**Topic search:**
```json
{
  "message": "Show me latest news about artificial intelligence"
}
```

**Current events:**
```json
{
  "message": "What's happening in technology today?"
}
```

### 4. Dictionary Lookups

**Word definition:**
```json
{
  "message": "What does 'ephemeral' mean?"
}
```

**Formal request:**
```json
{
  "message": "Define serendipity"
}
```

### 5. Currency Exchange

**Direct conversion:**
```json
{
  "message": "Convert 100 USD to EUR"
}
```

**Exchange rate:**
```json
{
  "message": "What's the exchange rate for GBP?"
}
```

### 6. Random Facts

```json
{
  "message": "Tell me an interesting fact"
}
```

```json
{
  "message": "Give me a random fact"
}
```

### 7. Wikipedia Information

```json
{
  "message": "Tell me about quantum computing"
}
```

```json
{
  "message": "What is machine learning?"
}
```

### 8. GitHub Repositories

```json
{
  "message": "Show me info about facebook/react repository"
}
```

```json
{
  "message": "Tell me about the microsoft/vscode repo"
}
```

## 🔄 Conversation Context Examples

### Example 1: Weather Follow-up

**First message:**
```json
{
  "message": "What's the weather in New York?"
}
```

**Response includes session_id:** `"session_id": "session-123"`

**Follow-up (remembers context):**
```json
{
  "message": "How about tomorrow?",
  "session_id": "session-123"
}
```

### Example 2: Comparison Queries

**First:**
```json
{
  "message": "What's Bitcoin's price?"
}
```

**Follow-up:**
```json
{
  "message": "How does that compare to Ethereum?",
  "session_id": "session-123"
}
```

## 🎯 Advanced Use Cases

### Use Case 1: Daily Briefing Bot

Create a bot that gives you a morning briefing:

```python
import requests

def morning_briefing():
    base_url = "http://localhost:8000/api/chat/message"
    
    queries = [
        "What's the weather in my city?",
        "Bitcoin price today?",
        "Latest tech news",
        "Tell me an interesting fact"
    ]
    
    for query in queries:
        response = requests.post(base_url, json={"message": query})
        print(f"\n{query}")
        print(response.json()["response"])
        print("-" * 50)

morning_briefing()
```

### Use Case 2: Multi-API Aggregator

Ask questions that require multiple APIs:

```json
{
  "message": "Give me weather in London, Bitcoin price, and latest AI news"
}
```

ConversAI will intelligently split this into multiple API calls.

### Use Case 3: Educational Assistant

```json
{
  "message": "Explain blockchain technology"
}
```

```json
{
  "message": "What are the latest developments in AI?"
}
```

### Use Case 4: Financial Dashboard

```python
import requests
import time

def financial_dashboard():
    """Get financial data every minute"""
    base_url = "http://localhost:8000/api/chat/message"
    
    while True:
        # Crypto prices
        crypto = requests.post(base_url, json={
            "message": "Show Bitcoin and Ethereum prices"
        }).json()
        
        # Exchange rates
        forex = requests.post(base_url, json={
            "message": "USD to EUR exchange rate"
        }).json()
        
        print(f"\n=== Financial Dashboard ===")
        print(crypto["response"])
        print(forex["response"])
        print(f"Time: {time.strftime('%H:%M:%S')}")
        
        time.sleep(60)  # Update every minute

# financial_dashboard()  # Uncomment to run
```

## 🛠️ Custom API Registration Example

Register your own API:

```python
import requests

custom_api = {
    "api_name": "JSONPlaceholder",
    "description": "Test API for fake data",
    "intent_keywords": ["user", "post", "placeholder"],
    "category": "testing",
    "endpoint": "https://jsonplaceholder.typicode.com/users/{id}",
    "method": "GET",
    "auth_config": {
        "type": "none"
    },
    "parameters": {
        "required": [
            {
                "name": "id",
                "type": "integer",
                "description": "User ID",
                "in_path": True,
                "default": "1"
            }
        ]
    },
    "response_mapping": {
        "name": "name",
        "email": "email",
        "company": "company.name"
    },
    "response_template": "User: {name}\nEmail: {email}\nCompany: {company}",
    "is_system": False
}

response = requests.post(
    "http://localhost:8000/api/apis/register",
    json=custom_api
)

print(response.json())
```

## 🔍 Testing Custom APIs

After registering, test your API:

```python
import requests

# Get the API ID from registration response
api_id = "your-api-id-here"

# Test the API
test_response = requests.post(
    f"http://localhost:8000/api/apis/{api_id}/test",
    json={
        "test_params": {
            "id": "5"
        }
    }
)

print(test_response.json())
```

## 📊 Analytics and Monitoring

### Get Conversation History

```python
import requests

session_id = "your-session-id"
history = requests.get(
    f"http://localhost:8000/api/chat/history/{session_id}"
)

for message in history.json():
    print(f"{message['role']}: {message['content']}\n")
```

### List All Available APIs

```python
import requests

apis = requests.get("http://localhost:8000/api/apis/list")

print("Available APIs:")
for api in apis.json():
    print(f"- {api['api_name']} ({api['category']})")
```

## 🎮 Interactive Python Script

Save this as `conversai_client.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"
session_id = None

def chat(message):
    global session_id
    
    payload = {"message": message}
    if session_id:
        payload["session_id"] = session_id
    
    response = requests.post(f"{BASE_URL}/chat/message", json=payload)
    result = response.json()
    
    # Save session ID for context
    session_id = result["session_id"]
    
    print(f"\n🤖 ConversAI: {result['response']}")
    print(f"📡 API Used: {result.get('api_used', 'N/A')}")
    print(f"💾 Cached: {result.get('cached', False)}")
    print(f"🎯 Intent: {result['intent']['intent']}")
    print(f"✅ Confidence: {result['intent']['confidence']:.2f}\n")

def main():
    print("=" * 60)
    print("ConversAI Interactive Client")
    print("=" * 60)
    print("Type 'quit' to exit, 'new' for new session, 'apis' to list APIs\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'new':
            session_id = None
            print("✨ New session started\n")
        elif user_input.lower() == 'apis':
            apis = requests.get(f"{BASE_URL}/apis/list").json()
            print("\n📋 Available APIs:")
            for api in apis:
                print(f"  - {api['api_name']}")
            print()
        elif user_input:
            try:
                chat(user_input)
            except Exception as e:
                print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    main()
```

**Run it:**
```bash
python conversai_client.py
```

## 🚀 Production Examples

### Example: Slack Bot Integration

```python
from slack_bolt import App
import requests

app = App(token="your-slack-token")

@app.message(".*")
def handle_message(message, say):
    user_text = message['text']
    
    # Send to ConversAI
    response = requests.post(
        "http://localhost:8000/api/chat/message",
        json={"message": user_text}
    ).json()
    
    say(response["response"])

app.start(port=3000)
```

### Example: Discord Bot

```python
import discord
import requests

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Send to ConversAI
    response = requests.post(
        "http://localhost:8000/api/chat/message",
        json={"message": message.content}
    ).json()
    
    await message.channel.send(response["response"])

client.run("your-discord-token")
```

### Example: Telegram Bot

```python
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters
import requests

def handle_message(update: Update, context):
    user_text = update.message.text
    
    # Send to ConversAI
    response = requests.post(
        "http://localhost:8000/api/chat/message",
        json={"message": user_text}
    ).json()
    
    update.message.reply_text(response["response"])

updater = Updater("your-telegram-token")
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
updater.start_polling()
```

## 📈 Performance Tips

### 1. Use Caching

Same queries within 5 minutes are cached:

```python
# First call - hits API (slower)
response1 = chat("Bitcoin price?")

# Second call within 1 minute - cached (instant)
response2 = chat("Bitcoin price?")
```

### 2. Batch Requests

For multiple independent queries:

```python
import asyncio
import aiohttp

async def batch_queries(queries):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for query in queries:
            task = session.post(
                "http://localhost:8000/api/chat/message",
                json={"message": query}
            )
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        return [await r.json() for r in responses]

queries = [
    "Weather in NYC",
    "Bitcoin price",
    "Latest news"
]

# Run all queries in parallel
results = asyncio.run(batch_queries(queries))
```

## 🎯 Error Handling

Always handle errors gracefully:

```python
import requests
from requests.exceptions import RequestException

def safe_chat(message):
    try:
        response = requests.post(
            "http://localhost:8000/api/chat/message",
            json={"message": message},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        return {
            "error": True,
            "message": f"Request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"Unexpected error: {str(e)}"
        }

# Usage
result = safe_chat("Hello!")
if result.get("error"):
    print(f"Error: {result['message']}")
else:
    print(result["response"])
```

---

**Need more examples?** Check the Swagger UI at http://localhost:8000/docs for interactive testing!
