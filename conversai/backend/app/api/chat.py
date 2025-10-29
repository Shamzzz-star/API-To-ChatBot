"""
Chat endpoints for ConversAI
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.schemas import ChatMessage, ChatResponse, MessageHistory
from app.core.database import get_db
from app.services.query_processor import QueryProcessor
from app.services.api_mapper import APIMapper
from app.services.api_handler import request_handler
from app.services.response_formatter import response_formatter
from app.models.database import Message, Conversation
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_msg: ChatMessage,
    db: Session = Depends(get_db)
):
    """
    Process a user message and return AI response
    
    Flow:
    1. Process query and extract intent
    2. Find matching API
    3. Prepare and send API request
    4. Format response naturally
    5. Save conversation
    """
    try:
        # Initialize services
        query_processor = QueryProcessor(db)
        api_mapper = APIMapper(db)
        
        # Get or create session
        session_id = chat_msg.session_id
        if not session_id:
            # For demo, use a default user_id (in production, get from auth)
            session_id = query_processor.create_session(user_id="demo-user")
        
        # Process query and extract intent
        intent_data = query_processor.process_query(chat_msg.message, session_id)
        
        # Check if clarification needed
        if intent_data.get("needs_clarification"):
            query_processor.save_message(
                session_id=session_id,
                role="assistant",
                content=intent_data["clarification_question"],
                metadata=intent_data
            )
            
            return ChatResponse(
                response=intent_data["clarification_question"],
                session_id=session_id,
                intent=intent_data,
                api_used=None,
                cached=False
            )
        
        # Find matching API
        api = api_mapper.find_matching_api(
            intent_data["intent"],
            intent_data.get("entities", {}),
            chat_msg.message  # Pass the original user query for better keyword matching
        )
        
        if not api:
            error_msg = "I couldn't find an appropriate API for your request. Please try rephrasing or register a custom API."
            query_processor.save_message(
                session_id=session_id,
                role="assistant",
                content=error_msg,
                metadata={"error": "no_api_found"}
            )
            
            return ChatResponse(
                response=error_msg,
                session_id=session_id,
                intent=intent_data,
                api_used=None,
                cached=False
            )
        
        # Prepare API request
        request_config = api_mapper.prepare_api_request(api, intent_data.get("entities", {}))
        
        if not request_config:
            error_msg = "Failed to prepare API request. Please check your input parameters."
            query_processor.save_message(
                session_id=session_id,
                role="assistant",
                content=error_msg,
                metadata={"error": "request_preparation_failed"}
            )
            
            return ChatResponse(
                response=error_msg,
                session_id=session_id,
                intent=intent_data,
                api_used=api.api_name,
                cached=False
            )
        
        # Send API request
        api_response = await request_handler.send_request(
            request_config=request_config,
            category=api.category
        )
        
        # Format response naturally
        try:
            formatted_response = await response_formatter.format_response(
                api_data=api_response,
                api=api,
                query=chat_msg.message,
                use_llm=True
            )
        except Exception as format_error:
            logger.error(f"Response formatting error: {format_error}", exc_info=True)
            logger.error(f"API response data: {api_response}")
            logger.error(f"API config: {api.api_name}, category: {api.category}")
            raise
        
        # Save assistant response
        query_processor.save_message(
            session_id=session_id,
            role="assistant",
            content=formatted_response,
            metadata={
                "intent": intent_data,
                "api_id": api.api_id,
                "api_name": api.api_name,
                "cached": api_response.get("_cached", False)
            }
        )
        
        return ChatResponse(
            response=formatted_response,
            session_id=session_id,
            intent=intent_data,
            api_used=api.api_name,
            cached=api_response.get("_cached", False)
        )
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )


@router.get("/history/{session_id}", response_model=List[MessageHistory])
async def get_conversation_history(
    session_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get conversation history for a session"""
    try:
        messages = db.query(Message).filter(
            Message.session_id == session_id
        ).order_by(
            Message.created_at.desc()
        ).limit(limit).all()
        
        # Reverse for chronological order
        messages = list(reversed(messages))
        
        return messages
        
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving history: {str(e)}"
        )


@router.delete("/session/{session_id}")
async def clear_conversation(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Clear/end a conversation session"""
    try:
        # End the conversation
        conversation = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).first()
        
        if conversation:
            conversation.ended_at = datetime.utcnow()
            db.commit()
            return {"message": "Conversation ended successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing conversation: {str(e)}"
        )


@router.post("/session/new")
async def create_new_session(
    db: Session = Depends(get_db)
):
    """Create a new conversation session"""
    try:
        query_processor = QueryProcessor(db)
        # For demo, use default user_id
        session_id = query_processor.create_session(user_id="demo-user")
        
        return {
            "session_id": session_id,
            "message": "New session created"
        }
        
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating session: {str(e)}"
        )
