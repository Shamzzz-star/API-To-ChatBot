"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str


# Chat schemas
class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    intent: Optional[Dict[str, Any]] = None
    api_used: Optional[str] = None
    cached: bool = False


class MessageHistory(BaseModel):
    message_id: str
    role: str
    content: str
    created_at: datetime
    message_metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True


# API Registry schemas
class APICreate(BaseModel):
    api_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    intent_keywords: List[str] = []
    category: Optional[str] = None
    endpoint: str = Field(..., min_length=1)
    method: str = Field(default="GET", pattern="^(GET|POST|PUT|DELETE)$")
    auth_config: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    response_mapping: Optional[Dict[str, Any]] = None
    response_template: Optional[str] = None
    rate_limit: Optional[Dict[str, Any]] = None
    error_messages: Optional[Dict[str, Any]] = None


class APIUpdate(BaseModel):
    api_name: Optional[str] = None
    description: Optional[str] = None
    intent_keywords: Optional[List[str]] = None
    category: Optional[str] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    auth_config: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    response_mapping: Optional[Dict[str, Any]] = None
    response_template: Optional[str] = None
    rate_limit: Optional[Dict[str, Any]] = None
    error_messages: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class APIResponse(BaseModel):
    api_id: str
    api_name: str
    description: Optional[str]
    category: Optional[str]
    intent_keywords: Optional[List[str]] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    auth_config: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    response_mapping: Optional[Dict[str, Any]] = None
    response_template: Optional[str] = None
    rate_limit: Optional[Dict[str, Any]] = None
    error_messages: Optional[Dict[str, Any]] = None
    is_active: bool
    is_system: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class APITestRequest(BaseModel):
    test_params: Dict[str, Any] = {}


class APITestResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# Analytics schemas
class UsageStats(BaseModel):
    total_messages: int
    total_api_calls: int
    popular_apis: List[Dict[str, Any]]
    success_rate: float
