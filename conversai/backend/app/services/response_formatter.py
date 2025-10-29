"""
Response Formatter - Formats API responses into natural language
"""
from typing import Dict, Any, Optional
from app.services.llm_service import llm_client
from app.models.database import APIRegistry
import json
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class ResponseFormatter:
    """Format API responses into natural, conversational language"""
    
    def __init__(self):
        self.llm = llm_client
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load response templates for common APIs"""
        return {
            "weather": "The weather in {city} is {condition} with a temperature of {temperature}°C (feels like {feels_like}°C). Humidity is {humidity}% and wind speed is {wind_speed} m/s.",
            "crypto": "{coin_name} is currently trading at ${price} USD. The 24-hour change is {change_24h}%.",
            "news": "Here are some recent news articles:\n{articles}",
            "dictionary": "**{word}** {phonetic}\n\n*{part_of_speech}*: {definition}\n\nExample: {example}",
            "exchange": "Current exchange rates for {base}: {rates}",
            "fact": "{fact}",
            "wikipedia": "**{title}**\n\n{extract}\n\nRead more: {url}",
            "github": "**{name}**\n{description}\n\n⭐ Stars: {stars} | Language: {language}\n{url}",
            "error": "I encountered an error: {error_message}"
        }
    
    async def format_response(
        self, 
        api_data: Dict[str, Any], 
        api: APIRegistry,
        query: str,
        use_llm: bool = True
    ) -> str:
        """
        Format API response into natural language
        
        Args:
            api_data: Raw API response
            api: API configuration
            query: Original user query
            use_llm: Whether to use LLM for formatting (fallback to templates)
        
        Returns:
            Formatted natural language response
        """
        # Handle errors
        if "error" in api_data:
            return self._format_error(api_data, api)
        
        # Check if API returned empty results (like empty matches array)
        if isinstance(api_data, dict):
            # Check for empty arrays in common result fields
            if "matches" in api_data and isinstance(api_data["matches"], list) and len(api_data["matches"]) == 0:
                logger.info(f"Empty results detected for {api.api_name}")
                return "I couldn't find any matches for your query. The API returned no results. This could mean there are no matches scheduled for the specified date or criteria."
            
            # Check for zero count
            if "resultSet" in api_data and isinstance(api_data["resultSet"], dict):
                if api_data["resultSet"].get("count", 0) == 0:
                    logger.info(f"Zero count detected for {api.api_name}")
                    return "No results found for your query. Try adjusting your search criteria or checking a different date."
        
        # Prioritize LLM-based formatting for natural responses
        if use_llm and self.llm.client:
            try:
                logger.info(f"Attempting LLM formatting for {api.api_name}")
                formatted = self.llm.generate_natural_response(api_data, query, api.api_name)
                return self._add_metadata(formatted, api, api_data)
            except Exception as e:
                logger.error(f"LLM formatting failed: {e}", exc_info=True)
        
        # Fallback to template-based formatting if LLM fails
        if api.response_template:
            try:
                logger.info(f"Fallback: Attempting template formatting for {api.api_name}")
                logger.debug(f"API data type: {type(api_data)}, keys: {api_data.keys() if isinstance(api_data, dict) else 'N/A'}")
                formatted = self._apply_template(api, api_data)
                if formatted:
                    return self._add_metadata(formatted, api, api_data)
            except Exception as e:
                logger.error(f"Template formatting failed for {api.api_name}: {e}", exc_info=True)
                logger.error(f"API data: {json.dumps(api_data, indent=2, default=str)}")
        
        # Last resort: category-based formatting
        try:
            logger.info(f"Attempting category-based formatting for {api.api_name}")
            return self._format_by_category(api.category, api_data, api)
        except Exception as e:
            logger.error(f"Category formatting failed: {e}", exc_info=True)
            return f"Error formatting response: {str(e)}"
    
    def _apply_template(self, api: APIRegistry, data: Dict[str, Any]) -> Optional[str]:
        """Apply response template with data mapping"""
        if not api.response_mapping:
            return None
        
        try:
            # Extract mapped values
            values = {}
            logger.info(f"Extracting values from data for {api.api_name}")
            logger.info(f"Response mapping: {api.response_mapping}")
            logger.info(f"Data structure: {json.dumps(data, indent=2, default=str)[:1000]}")
            
            for key, path in api.response_mapping.items():
                value = self._extract_value_by_path(data, path)
                logger.info(f"Extracted '{key}' from path '{path}': {value}")
                values[key] = value if value is not None else "N/A"
            
            logger.info(f"Final extracted values: {values}")
            
            # Apply template
            template = api.response_template
            formatted_result = template.format(**values)
            logger.info(f"Formatted result: {formatted_result}")
            return formatted_result
            
        except (KeyError, TypeError, AttributeError) as e:
            logger.warning(f"Template application failed for {api.api_name}: {e}")
            return None
    
    def _extract_value_by_path(self, data: Dict[str, Any], path: str) -> Any:
        """Extract value from nested dict/list using dot notation and array indices"""
        try:
            current = data
            
            # Parse path with array indices and dot notation
            # Example: "[0].word" or "data.items[0].name"
            # Split by dot, keeping array indices with their keys
            parts = re.split(r'\.(?![^\[]*\])', path)
            
            logger.debug(f"Extracting path '{path}' from data type: {type(data)}")
            logger.debug(f"Split into parts: {parts}")
            
            for part in parts:
                # Check if part contains array index like "[0]" or "items[0]"
                array_match = re.match(r'^(\w*)\[(\d+)\]$', part)
                if array_match:
                    key, index = array_match.groups()
                    if key:
                        current = current[key]
                    current = current[int(index)]
                elif part:
                    current = current[part]
            
            return current
            
        except (KeyError, IndexError, TypeError, AttributeError) as e:
            logger.error(f"Could not extract value at path '{path}' from data: {e}")
            logger.error(f"Current data type: {type(data)}, path: {path}")
            return None
    
    def _format_by_category(self, category: str, data: Dict[str, Any], api: APIRegistry) -> str:
        """Format response based on category"""
        if category == "weather":
            return self._format_weather(data)
        elif category == "cryptocurrency":
            return self._format_crypto(data)
        elif category == "news":
            return self._format_news(data)
        elif category == "dictionary":
            return self._format_dictionary(data)
        elif category == "finance":
            return self._format_exchange(data)
        elif category == "entertainment":
            return self._format_fact(data)
        elif category == "knowledge":
            return self._format_wikipedia(data)
        elif category == "development":
            return self._format_github(data)
        else:
            return self._format_generic(data, api)
    
    def _format_weather(self, data: Dict) -> str:
        """Format weather data"""
        try:
            city = data.get("name", "Unknown")
            temp = data.get("main", {}).get("temp", "N/A")
            condition = data.get("weather", [{}])[0].get("description", "N/A")
            humidity = data.get("main", {}).get("humidity", "N/A")
            
            return f"The weather in {city} is {condition} with a temperature of {temp}°C. Humidity is {humidity}%."
        except Exception as e:
            logger.error(f"Weather formatting error: {e}")
            return f"Weather data: {json.dumps(data, indent=2)}"
    
    def _format_crypto(self, data: Dict) -> str:
        """Format cryptocurrency data"""
        try:
            # CoinGecko format: {"bitcoin": {"usd": 45000, "usd_24h_change": 2.5}}
            coin = list(data.keys())[0] if data else "unknown"
            price = data.get(coin, {}).get("usd", "N/A")
            change = data.get(coin, {}).get("usd_24h_change", "N/A")
            
            return f"{coin.title()} is currently trading at ${price:,.2f} USD. 24-hour change: {change:.2f}%."
        except Exception as e:
            logger.error(f"Crypto formatting error: {e}")
            return f"Cryptocurrency data: {json.dumps(data, indent=2)}"
    
    def _format_news(self, data: Dict) -> str:
        """Format news data"""
        try:
            articles = data.get("articles", [])[:5]
            if not articles:
                return "No news articles found."
            
            formatted = "Here are some recent news articles:\n\n"
            for i, article in enumerate(articles, 1):
                title = article.get("title", "No title")
                source = article.get("source", {}).get("name", "Unknown")
                url = article.get("url", "")
                formatted += f"{i}. **{title}** - {source}\n   {url}\n\n"
            
            return formatted
        except Exception as e:
            logger.error(f"News formatting error: {e}")
            return f"News data: {json.dumps(data, indent=2)}"
    
    def _format_dictionary(self, data: Dict) -> str:
        """Format dictionary data"""
        try:
            if isinstance(data, list) and len(data) > 0:
                entry = data[0]
                word = entry.get("word", "")
                phonetic = entry.get("phonetic", "")
                meanings = entry.get("meanings", [])
                
                if meanings:
                    meaning = meanings[0]
                    pos = meaning.get("partOfSpeech", "")
                    definitions = meaning.get("definitions", [])
                    
                    if definitions:
                        definition = definitions[0].get("definition", "")
                        example = definitions[0].get("example", "")
                        
                        result = f"**{word}** {phonetic}\n\n*{pos}*: {definition}"
                        if example:
                            result += f"\n\nExample: {example}"
                        return result
            
            return f"Definition: {json.dumps(data, indent=2)}"
        except Exception as e:
            logger.error(f"Dictionary formatting error: {e}")
            return f"Dictionary data: {json.dumps(data, indent=2)}"
    
    def _format_exchange(self, data: Dict) -> str:
        """Format exchange rate data"""
        try:
            base = data.get("base", "USD")
            rates = data.get("rates", {})
            
            # Show top 10 currencies
            popular = ["EUR", "GBP", "JPY", "INR", "CAD", "AUD", "CHF", "CNY", "MXN", "BRL"]
            formatted = f"Exchange rates for {base}:\n\n"
            
            for currency in popular:
                if currency in rates:
                    formatted += f"1 {base} = {rates[currency]:.4f} {currency}\n"
            
            return formatted
        except Exception as e:
            logger.error(f"Exchange formatting error: {e}")
            return f"Exchange rate data: {json.dumps(data, indent=2)}"
    
    def _format_fact(self, data: Dict) -> str:
        """Format fact data"""
        try:
            if isinstance(data, list) and len(data) > 0:
                return f"Here's an interesting fact: {data[0].get('fact', '')}"
            return f"Fact: {json.dumps(data)}"
        except Exception as e:
            logger.error(f"Fact formatting error: {e}")
            return f"Fact data: {json.dumps(data, indent=2)}"
    
    def _format_wikipedia(self, data: Dict) -> str:
        """Format Wikipedia data"""
        try:
            title = data.get("title", "")
            extract = data.get("extract", "")
            url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
            
            return f"**{title}**\n\n{extract}\n\nRead more: {url}"
        except Exception as e:
            logger.error(f"Wikipedia formatting error: {e}")
            return f"Wikipedia data: {json.dumps(data, indent=2)}"
    
    def _format_github(self, data: Dict) -> str:
        """Format GitHub repository data"""
        try:
            name = data.get("name", "")
            description = data.get("description", "No description")
            stars = data.get("stargazers_count", 0)
            language = data.get("language", "N/A")
            url = data.get("html_url", "")
            
            return f"**{name}**\n{description}\n\n⭐ Stars: {stars:,} | Language: {language}\n{url}"
        except Exception as e:
            logger.error(f"GitHub formatting error: {e}")
            return f"GitHub data: {json.dumps(data, indent=2)}"
    
    def _format_generic(self, data: Dict, api: APIRegistry) -> str:
        """Generic formatting for unknown categories"""
        return f"Data from {api.api_name}:\n\n```json\n{json.dumps(data, indent=2)}\n```"
    
    def _format_error(self, error_data: Dict, api: APIRegistry) -> str:
        """Format error messages using LLM for natural responses"""
        error_msg = error_data.get("error", "Unknown error")
        status_code = error_data.get("status_code")
        
        # Try to generate a natural error response using LLM
        if self.llm.client:
            try:
                logger.info(f"Generating natural error message for {api.api_name}")
                
                # Create context for LLM
                error_context = {
                    "api_name": api.api_name,
                    "error_message": error_msg,
                    "status_code": status_code,
                    "api_description": api.description
                }
                
                prompt = f"""The user tried to query the {api.api_name} API but encountered an error.
                
Error Details:
- API: {api.api_name} ({api.description})
- Error: {error_msg}
- Status Code: {status_code}

Generate a helpful, conversational response that:
1. Explains what went wrong in simple, non-technical terms
2. Suggests what the user might need to provide (e.g., "a city name" for weather, "a specific date", "a team name", etc.)
3. Gives a simple example of a better query using natural language (e.g., "try asking 'weather in London'" or "what's the weather in New York")
4. Keep it friendly and concise (2-3 sentences max)

IMPORTANT RULES:
- DO NOT include API URLs, endpoints, or technical implementation details
- DO NOT mention HTTP status codes, parameters, or API keys
- DO NOT show code examples or curl commands
- DO use natural, conversational language like you're talking to a friend
- DO give simple, user-friendly query examples in quotes"""

                response = self.llm.client.chat.completions.create(
                    model=self.llm.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that explains API errors in a friendly, conversational way."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                
                natural_response = response.choices[0].message.content.strip()
                logger.info(f"Generated natural error message: {natural_response}")
                return natural_response
                
            except Exception as e:
                logger.error(f"LLM error formatting failed: {e}", exc_info=True)
        
        # Fallback: Check for custom error messages in API config
        if api.error_messages and status_code:
            custom_msg = api.error_messages.get(str(status_code))
            if custom_msg:
                return f"❌ {custom_msg}"
        
        # Last resort: simple error message
        return f"❌ I encountered an error while fetching data: {error_msg}"
    
    def _add_metadata(self, response: str, api: APIRegistry, data: Dict) -> str:
        """Add source attribution and timestamp"""
        cached = data.get("_cached", False)
        cache_indicator = "📦 (cached)" if cached else ""
        
        timestamp = datetime.now().strftime("%I:%M %p")
        metadata = f"\n\n---\n*Data from {api.api_name} {cache_indicator} • {timestamp}*"
        
        return response + metadata


# Global formatter instance
response_formatter = ResponseFormatter()
