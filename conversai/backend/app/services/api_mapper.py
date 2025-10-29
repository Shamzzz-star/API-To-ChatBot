"""
API Mapper - Maps intents to APIs and prepares API requests
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.database import APIRegistry
from app.config.free_apis import FREE_APIS
from app.core.security import encryption_service
from app.core.config import settings
from datetime import datetime, timedelta
import re
import logging

logger = logging.getLogger(__name__)


class APIMapper:
    """Map user intents to appropriate APIs"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ensure_system_apis_loaded()
    
    def ensure_system_apis_loaded(self):
        """Load system (free) APIs into database if not already present"""
        try:
            for api_config in FREE_APIS:
                existing = self.db.query(APIRegistry).filter(
                    APIRegistry.api_id == api_config["api_id"]
                ).first()
                
                if not existing:
                    api = APIRegistry(**api_config)
                    self.db.add(api)
            
            self.db.commit()
            logger.info(f"✅ Loaded {len(FREE_APIS)} system APIs")
            
        except Exception as e:
            logger.error(f"Error loading system APIs: {e}")
            self.db.rollback()
    
    def find_matching_api(self, intent: str, entities: Dict[str, Any], user_query: str = "") -> Optional[APIRegistry]:
        """
        Find the best matching API for given intent
        
        Args:
            intent: The classified intent (e.g., "weather", "news", "sports")
            entities: Extracted entities from the query
            user_query: The original user query text for keyword matching
        """
        try:
            # Reload all active APIs from database (includes newly added user APIs)
            apis = self.db.query(APIRegistry).filter(
                APIRegistry.is_active == True
            ).all()
            
            logger.info(f"✅ Loaded {len(apis)} active APIs from database (system + user)")
            
            best_match = None
            best_score = 0
            
            # Use user query for matching if available, otherwise use intent
            match_text = (user_query or intent).lower()
            
            # First try keyword matching - this is more specific
            for api in apis:
                if api.intent_keywords:
                    score = sum(1 for keyword in api.intent_keywords if keyword.lower() in match_text)
                    if score > best_score:
                        best_score = score
                        best_match = api
            
            # If we found a good keyword match, return it
            if best_match and best_score > 0:
                logger.info(f"✅ Found API by keyword match: {best_match.api_name} (score: {best_score}, category: {best_match.category})")
                return best_match
            
            # Fall back to category mapping if no keyword match
            category_map = {
                "weather": "weather",
                "crypto": "cryptocurrency",
                "news": "news",
                "dictionary": "dictionary",
                "exchange": "finance",
                "fact": "entertainment",
                "wikipedia": "knowledge",
                "github": "development",
                "sports": "sports",
                "team": "sports",
                "score": "sports",
                "match": "sports"
            }
            
            category = category_map.get(intent)
            if category:
                api = self.db.query(APIRegistry).filter(
                    APIRegistry.category == category,
                    APIRegistry.is_active == True
                ).first()
                
                if api:
                    logger.info(f"✅ Found API by category match: {api.api_name} (category: {category})")
                    return api
            
            logger.warning(f"❌ No matching API found for intent: {intent}, query: {user_query}")
            return None
            
        except Exception as e:
            logger.error(f"Error finding matching API: {e}")
            return None
    
    def prepare_api_request(self, api: APIRegistry, entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare API request with parameters from extracted entities
        
        Returns:
            {
                "url": "full URL",
                "method": "GET/POST",
                "headers": {},
                "params": {},
                "data": {}
            }
        """
        try:
            # Build base URL
            url = api.endpoint
            
            # Initialize request components
            headers = {}
            params = {}
            data = {}
            
            # Handle authentication
            if api.auth_config and api.auth_config.get("type") != "none":
                auth_type = api.auth_config.get("type")
                
                if auth_type == "api_key":
                    param_name = api.auth_config.get("param_name")
                    param_location = api.auth_config.get("param_location", "query")
                    
                    # Get API key from settings or database
                    api_key = self._get_api_key(api.api_id)
                    
                    if api_key:
                        if param_location == "header":
                            headers[param_name] = api_key
                        else:
                            params[param_name] = api_key
            
            # Map entities to API parameters
            if api.parameters:
                # Required parameters
                for param in api.parameters.get("required", []):
                    param_name = param["name"]
                    
                    # Check if parameter is in URL path
                    if param.get("in_path"):
                        value = self._extract_param_value(param, entities)
                        logger.info(f"Extracted value for '{param_name}' (in_path): {value} from entities: {entities}")
                        if value:
                            # For dictionary API, handle multi-word terms by taking first word
                            if param_name == "word" and " " in str(value):
                                logger.info(f"Multi-word detected: '{value}', taking first word")
                                value = str(value).split()[0]
                            # URL encode the value for path parameters
                            from urllib.parse import quote
                            encoded_value = quote(str(value), safe='')
                            logger.info(f"Replacing {{{param_name}}} with '{encoded_value}' in URL: {url}")
                            url = url.replace(f"{{{param_name}}}", encoded_value)
                            logger.info(f"URL after replacement: {url}")
                        else:
                            logger.warning(f"No value extracted for required path parameter '{param_name}'")
                    else:
                        value = self._extract_param_value(param, entities)
                        if value:
                            params[param_name] = value
                        elif not param.get("default"):
                            logger.warning(f"Missing required parameter: {param_name}")
                
                # Optional parameters
                for param in api.parameters.get("optional", []):
                    param_name = param["name"]
                    value = self._extract_param_value(param, entities)
                    
                    if value:
                        params[param_name] = value
                    elif "default" in param:
                        params[param_name] = param["default"]
            
            return {
                "url": url,
                "method": api.method or "GET",
                "headers": headers,
                "params": params,
                "data": data
            }
            
        except Exception as e:
            logger.error(f"Error preparing API request: {e}")
            return None
    
    def _get_api_key(self, api_id: str) -> Optional[str]:
        """Get API key for a given API"""
        # Map API IDs to environment variable keys
        key_map = {
            "weather-openweather": settings.OPENWEATHER_API_KEY,
            "news-newsapi": settings.NEWSAPI_KEY,
            "facts-ninja": settings.API_NINJAS_KEY,
        }
        
        return key_map.get(api_id)
    
    def _extract_param_value(self, param: Dict, entities: Dict) -> Optional[Any]:
        """Extract parameter value from entities"""
        param_name = param["name"]
        
        # Handle automatic date parameters FIRST (before direct mapping)
        if param_name in ['d', 'date', 'day']:
            # Check if user provided a specific date
            date_value = entities.get('date') or entities.get('day')
            if date_value:
                # Convert natural language dates to YYYY-MM-DD format
                date_str = str(date_value).lower()
                if date_str == 'today':
                    date_value = datetime.now().strftime('%Y-%m-%d')
                elif date_str == 'yesterday':
                    date_value = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                elif date_str == 'tomorrow':
                    date_value = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
                logger.info(f"Converted date '{date_str}' to: {date_value}")
                return date_value
            # Don't auto-generate date if not explicitly provided
            # This allows team-based queries to return latest matches
            logger.info(f"No date specified, skipping date parameter")
            return None
        
        # Try direct entity mapping (for non-date parameters)
        if param_name in entities:
            logger.info(f"Direct mapping found: {param_name} = {entities[param_name]}")
            return entities[param_name]
        
        # Handle sport/league parameters
        if param_name in ['s', 'sport', 'league']:
            sport = entities.get('sport') or entities.get('league') or entities.get('keyword')
            if sport:
                # If keyword contains sport name, extract it
                sport_str = str(sport).lower()
                if 'soccer' in sport_str or 'football' in sport_str:
                    return 'Soccer'
                elif 'basketball' in sport_str:
                    return 'Basketball'
                elif 'baseball' in sport_str:
                    return 'Baseball'
                elif 'hockey' in sport_str:
                    return 'Ice Hockey'
                return sport
            # Default to Soccer for sports queries
            return 'Soccer'
        
        # Try common mappings
        mappings = {
            "q": entities.get("location") or entities.get("keyword"),
            "city": entities.get("location"),
            "ids": entities.get("coin"),
            "word": entities.get("word") or entities.get("keyword"),
            "base": entities.get("from_currency"),
            "title": entities.get("keyword"),
            "owner": entities.get("owner"),
            "repo": entities.get("repo"),
            "t": entities.get("keyword") or entities.get("team")  # Sports team name
        }
        
        if param_name in mappings:
            value = mappings[param_name]
            
            # Clean up sports team names - remove common words like "team", "fc", "club"
            if param_name == "t" and value:
                cleanup_words = [" team", " fc", " club", " squad"]
                value_str = str(value)
                for word in cleanup_words:
                    value_str = value_str.replace(word, "").strip()
                value = value_str
            
            logger.info(f"Mapped parameter '{param_name}' to value: {value}")
            return value
        
        logger.warning(f"No mapping found for parameter '{param_name}' in entities: {entities}")
        return None
    
    def validate_parameters(self, api: APIRegistry, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate that all required parameters are present
        
        Returns:
            (is_valid, error_message)
        """
        if not api.parameters:
            return True, None
        
        required_params = api.parameters.get("required", [])
        
        for param in required_params:
            param_name = param["name"]
            if param_name not in params and not param.get("default"):
                return False, f"Missing required parameter: {param_name}"
        
        return True, None
