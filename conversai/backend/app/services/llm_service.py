"""
LLM Client for intent extraction and response generation using Groq API (FREE)
"""
from groq import Groq
from app.core.config import settings
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json
import re
import logging

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for interacting with Groq's free LLM API"""
    
    def __init__(self):
        if not settings.GROQ_API_KEY:
            logger.warning("GROQ_API_KEY not set. LLM features will be limited.")
            self.client = None
        else:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
    
    def extract_intent(self, query: str, context: list = None) -> Dict[str, Any]:
        """
        Extract intent and entities from user query using LLM
        
        Returns:
            {
                "intent": "weather|crypto|news|dictionary|exchange|custom",
                "confidence": 0.0-1.0,
                "entities": {...},
                "needs_clarification": bool,
                "clarification_question": str
            }
        """
        if not self.client:
            return self._fallback_intent_extraction(query)
        
        # Build context string
        context_str = ""
        if context:
            context_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context[-3:]])
        
        prompt = f"""You are an intent classifier for an API interaction system.
Analyze the user query and extract the following in JSON format:

{{
  "intent": "weather|crypto|news|dictionary|exchange|fact|wikipedia|github|sports|score|match|custom",
  "confidence": 0.0-1.0,
  "entities": {{
    "location": "city name if mentioned",
    "coin": "cryptocurrency if mentioned (bitcoin, ethereum, etc)",
    "keyword": "search term or topic",
    "date": "date if mentioned (today, tomorrow, or YYYY-MM-DD)",
    "sport": "sport type if mentioned (Soccer, Basketball, etc)",
    "team": "team name if mentioned",
    "from_currency": "source currency for exchange",
    "to_currency": "target currency for exchange",
    "amount": "amount to convert",
    "word": "word to define",
    "parameters": {{}}
  }},
  "needs_clarification": true|false,
  "clarification_question": "question to ask if clarification needed"
}}

Available intents:
- weather: Weather information for a location
- crypto: Cryptocurrency prices (bitcoin, ethereum, etc)
- news: News articles on a topic
- dictionary: Word definitions
- exchange: Currency exchange rates
- fact: Random interesting facts
- wikipedia: Wikipedia information
- github: GitHub repository information
- sports: Information about sports teams
- score: Live scores or match results
- match: Match information or fixtures
- custom: Other API queries

Recent conversation context:
{context_str}

User Query: {query}

Return ONLY valid JSON, no explanation."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            result = json.loads(result_text)
            
            # Validate and set defaults
            result.setdefault("confidence", 0.7)
            result.setdefault("needs_clarification", False)
            result.setdefault("clarification_question", "")
            result.setdefault("entities", {})
            
            # Extract date from the original query if not already present
            if "date" not in result["entities"] or not result["entities"]["date"]:
                extracted_date = self._extract_date_from_query(query)
                if extracted_date:
                    result["entities"]["date"] = extracted_date
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return self._fallback_intent_extraction(query)
        except Exception as e:
            logger.error(f"LLM intent extraction error: {e}")
            return self._fallback_intent_extraction(query)
    
    def _fallback_intent_extraction(self, query: str) -> Dict[str, Any]:
        """Rule-based fallback when LLM is unavailable"""
        query_lower = query.lower()
        
        # Simple keyword matching
        if any(word in query_lower for word in ["weather", "temperature", "forecast", "rain", "sunny"]):
            return {
                "intent": "weather",
                "confidence": 0.6,
                "entities": self._extract_location(query),
                "needs_clarification": "location" not in self._extract_location(query),
                "clarification_question": "Which city would you like weather for?"
            }
        elif any(word in query_lower for word in ["bitcoin", "btc", "ethereum", "eth", "crypto", "coin", "price"]):
            return {
                "intent": "crypto",
                "confidence": 0.7,
                "entities": {"coin": self._extract_crypto(query)},
                "needs_clarification": False
            }
        elif any(word in query_lower for word in ["news", "article", "headline", "latest"]):
            return {
                "intent": "news",
                "confidence": 0.6,
                "entities": {"keyword": self._extract_keyword(query)},
                "needs_clarification": False
            }
        elif any(word in query_lower for word in ["define", "definition", "meaning", "what is", "what does"]):
            return {
                "intent": "dictionary",
                "confidence": 0.7,
                "entities": {"word": self._extract_word(query)},
                "needs_clarification": False
            }
        elif any(word in query_lower for word in ["convert", "exchange", "rate", "usd", "eur", "currency"]):
            return {
                "intent": "exchange",
                "confidence": 0.6,
                "entities": self._extract_currencies(query),
                "needs_clarification": False
            }
        else:
            return {
                "intent": "custom",
                "confidence": 0.4,
                "entities": {},
                "needs_clarification": True,
                "clarification_question": "I'm not sure what you're looking for. Can you be more specific?"
            }
    
    def _extract_location(self, query: str) -> dict:
        """Extract location from query"""
        # Simple extraction - in production, use NER
        words = query.split()
        for i, word in enumerate(words):
            if word.lower() in ["in", "at", "for"]:
                if i + 1 < len(words):
                    return {"location": " ".join(words[i+1:]).strip("?.,!").title()}
        return {}
    
    def _extract_crypto(self, query: str) -> str:
        """Extract cryptocurrency from query"""
        query_lower = query.lower()
        crypto_map = {
            "bitcoin": "bitcoin", "btc": "bitcoin",
            "ethereum": "ethereum", "eth": "ethereum",
            "dogecoin": "dogecoin", "doge": "dogecoin",
            "cardano": "cardano", "ada": "cardano",
            "ripple": "ripple", "xrp": "ripple"
        }
        
        for key, value in crypto_map.items():
            if key in query_lower:
                return value
        return "bitcoin"
    
    def _extract_keyword(self, query: str) -> str:
        """Extract keyword for news search"""
        stop_words = {"news", "about", "on", "latest", "show", "me", "get", "find", "the", "a", "an"}
        words = [w.strip("?.,!") for w in query.lower().split() if w not in stop_words]
        return " ".join(words[:3]) if words else "technology"
    
    def _extract_word(self, query: str) -> str:
        """Extract word to define"""
        query_lower = query.lower()
        for phrase in ["define ", "definition of ", "what is ", "what does ", "meaning of "]:
            if phrase in query_lower:
                word = query_lower.split(phrase)[-1].strip("?.,!")
                return word.split()[0]
        words = query.split()
        return words[-1].strip("?.,!") if words else "example"
    
    def _extract_currencies(self, query: str) -> dict:
        """Extract currency codes from query"""
        # Simple extraction
        common_currencies = ["USD", "EUR", "GBP", "JPY", "INR", "CAD", "AUD"]
        found = [curr for curr in common_currencies if curr.lower() in query.lower()]
        
        if len(found) >= 2:
            return {"from_currency": found[0], "to_currency": found[1]}
        elif len(found) == 1:
            return {"from_currency": found[0], "to_currency": "USD"}
        return {"from_currency": "USD", "to_currency": "EUR"}
    
    def generate_natural_response(self, api_data: dict, query: str, api_name: str) -> str:
        """
        Generate a natural language response from API data using LLM
        """
        if not self.client:
            return self._format_simple_response(api_data, api_name)
        
        prompt = f"""Convert this API response into a natural, conversational answer.

User Question: {query}
API Response: {json.dumps(api_data, indent=2)}
Data Source: {api_name}

Generate a concise, friendly response (2-3 sentences max).
Do not make up information. Only use data from the API response.
If there's an error, explain it clearly."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"LLM response generation error: {e}")
            return self._format_simple_response(api_data, api_name)
    
    def _format_simple_response(self, data: dict, api_name: str) -> str:
        """Simple fallback response formatting"""
        if "error" in data:
            return f"I encountered an error: {data['error']}"
        return f"Here's the data from {api_name}: {json.dumps(data, indent=2)}"
    
    def _extract_date_from_query(self, query: str) -> Optional[str]:
        """Extract date from natural language in the query"""
        query_lower = query.lower()
        
        # Check for "today"
        if 'today' in query_lower or 'tonight' in query_lower:
            return datetime.now().strftime('%Y-%m-%d')
        
        # Check for "yesterday"
        if 'yesterday' in query_lower:
            return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Check for "tomorrow"
        if 'tomorrow' in query_lower:
            return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Check for "this week" or "this weekend"
        if 'this week' in query_lower or 'this weekend' in query_lower:
            return datetime.now().strftime('%Y-%m-%d')
        
        # Check for specific date patterns (YYYY-MM-DD, MM/DD/YYYY, etc.)
        date_patterns = [
            (r'\d{4}-\d{2}-\d{2}', '%Y-%m-%d'),  # YYYY-MM-DD
            (r'\d{2}/\d{2}/\d{4}', '%m/%d/%Y'),  # MM/DD/YYYY
            (r'\d{2}-\d{2}-\d{4}', '%d-%m-%Y'),  # DD-MM-YYYY
        ]
        
        for pattern, date_format in date_patterns:
            match = re.search(pattern, query)
            if match:
                date_str = match.group(0)
                try:
                    parsed = datetime.strptime(date_str, date_format)
                    return parsed.strftime('%Y-%m-%d')
                except:
                    continue
        
        return None


# Global LLM client instance
llm_client = LLMClient()
