"""
Main FastAPI application for ConversAI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api import chat, api_management
import logging

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Natural Language Chatbot for Seamless API Interaction",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(chat.router, prefix="/api")
app.include_router(api_management.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Initialize database and load system APIs on startup"""
    logger.info("Starting ConversAI...")
    init_db()
    logger.info("✅ ConversAI is ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down ConversAI...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to ConversAI API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


@app.get("/api/info")
async def api_info():
    """API information"""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "llm_model": settings.GROQ_MODEL,
        "features": [
            "Natural language API interaction",
            "8+ pre-configured free APIs",
            "Custom API registration",
            "Conversation context management",
            "Response caching",
            "Intent classification"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
