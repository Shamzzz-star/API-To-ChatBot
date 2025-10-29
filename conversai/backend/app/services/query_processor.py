"""
Query Processor - Handles user input, context management, and intent extraction
"""
from typing import Dict, Any, List, Optional
from app.services.llm_service import llm_client
from app.models.database import Message, Conversation
from sqlalchemy.orm import Session
import logging
import re

logger = logging.getLogger(__name__)


class QueryProcessor:
    """Process user queries and extract intents"""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm = llm_client
    
    def process_query(self, user_input: str, session_id: str) -> Dict[str, Any]:
        """
        Process a user query:
        1. Retrieve conversation context
        2. Sanitize input
        3. Extract intent using LLM
        4. Return structured intent object
        """
        # Sanitize input
        sanitized_input = self.sanitize_input(user_input)
        
        # Get conversation context
        context = self.get_conversation_context(session_id)
        
        # Extract intent using LLM
        intent_data = self.llm.extract_intent(sanitized_input, context)
        
        # Save user message
        self.save_message(session_id, "user", sanitized_input, intent_data)
        
        return intent_data
    
    def sanitize_input(self, user_input: str) -> str:
        """
        Sanitize user input to prevent XSS, SQL injection, etc.
        """
        if not user_input:
            return ""
        
        # Remove potential HTML/script tags
        sanitized = re.sub(r'<[^>]*>', '', user_input)
        
        # Remove excessive whitespace
        sanitized = ' '.join(sanitized.split())
        
        # Limit length
        max_length = 1000
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized.strip()
    
    def get_conversation_context(self, session_id: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Retrieve recent conversation context for better intent understanding
        """
        try:
            messages = self.db.query(Message).filter(
                Message.session_id == session_id
            ).order_by(
                Message.created_at.desc()
            ).limit(limit).all()
            
            # Reverse to get chronological order
            messages = list(reversed(messages))
            
            context = []
            for msg in messages:
                context.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            return context
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    def save_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict] = None):
        """Save a message to the database"""
        try:
            message = Message(
                session_id=session_id,
                role=role,
                content=content,
                message_metadata=metadata
            )
            self.db.add(message)
            
            # Update message count
            conversation = self.db.query(Conversation).filter(
                Conversation.session_id == session_id
            ).first()
            
            if conversation:
                conversation.message_count += 1
            
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            self.db.rollback()
    
    def create_session(self, user_id: str) -> str:
        """Create a new conversation session"""
        try:
            conversation = Conversation(user_id=user_id)
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
            return conversation.session_id
            
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            self.db.rollback()
            raise
    
    def end_session(self, session_id: str):
        """End a conversation session"""
        try:
            from datetime import datetime
            conversation = self.db.query(Conversation).filter(
                Conversation.session_id == session_id
            ).first()
            
            if conversation:
                conversation.ended_at = datetime.utcnow()
                self.db.commit()
                
        except Exception as e:
            logger.error(f"Error ending session: {e}")
            self.db.rollback()
