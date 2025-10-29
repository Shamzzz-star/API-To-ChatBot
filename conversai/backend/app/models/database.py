"""
Database models for ConversAI
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid


Base = declarative_base()


def generate_uuid():
    """Generate a UUID string"""
    return str(uuid.uuid4())


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    apis = relationship("APIRegistry", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    usage_logs = relationship("APIUsageLog", back_populates="user", cascade="all, delete-orphan")


class APIRegistry(Base):
    """API Registry model for storing custom and pre-configured APIs"""
    __tablename__ = "api_registry"
    
    api_id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=True)
    api_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    intent_keywords = Column(JSON, nullable=True)  # List of keywords
    category = Column(String(50), nullable=True)
    endpoint = Column(Text, nullable=False)
    method = Column(String(10), default="GET")
    auth_config = Column(JSON, nullable=True)
    parameters = Column(JSON, nullable=True)
    response_mapping = Column(JSON, nullable=True)
    response_template = Column(Text, nullable=True)
    rate_limit = Column(JSON, nullable=True)
    error_messages = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    is_system = Column(Boolean, default=False)  # System pre-configured APIs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="apis")
    usage_logs = relationship("APIUsageLog", back_populates="api", cascade="all, delete-orphan")


class Conversation(Base):
    """Conversation/Session model"""
    __tablename__ = "conversations"
    
    session_id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    message_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """Message model"""
    __tablename__ = "messages"
    
    message_id = Column(String, primary_key=True, default=generate_uuid)
    session_id = Column(String, ForeignKey("conversations.session_id"), nullable=False)
    role = Column(String(10), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    message_metadata = Column(JSON, nullable=True)  # Store intent, api_used, etc.
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class APIUsageLog(Base):
    """API Usage Logs for analytics"""
    __tablename__ = "api_usage_logs"
    
    log_id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    api_id = Column(String, ForeignKey("api_registry.api_id"), nullable=False)
    query = Column(Text, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    status = Column(String(20), nullable=False)  # 'success', 'error', 'cached'
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="usage_logs")
    api = relationship("APIRegistry", back_populates="usage_logs")
