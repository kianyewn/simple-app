"""
FastAPI backend application for Simple Groq App.

This module contains the main FastAPI application with Groq integration.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from backend.models.chat_models import ChatRequest, ChatResponse, HealthResponse
from backend.services.groq_service import GroqService
from backend.utils.config import config


# Initialize FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description="A simple application using FastAPI backend with Groq AI integration",
    docs_url="/docs" if config.DEBUG else None,
    redoc_url="/redoc" if config.DEBUG else None
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Initialize Groq service
groq_service = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup."""
    global groq_service
    
    # Validate configuration
    if not config.validate_config():
        raise RuntimeError("Invalid configuration. Please check environment variables.")
    
    # Initialize Groq service
    try:
        groq_service = GroqService(api_key=config.GROQ_API_KEY)
        print(f"✅ {config.APP_NAME} started successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize Groq service: {str(e)}")
        raise RuntimeError(f"Failed to initialize Groq service: {str(e)}")


@app.get("/", response_model=HealthResponse)
async def root():
    """
    Root endpoint for basic health check.
    
    Returns:
        HealthResponse: Basic application information.
    """
    return HealthResponse(
        status="healthy",
        message=f"Welcome to {config.APP_NAME}!",
        version=config.APP_VERSION
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Detailed health status.
    """
    return HealthResponse(
        status="healthy",
        message="Application is running smoothly",
        version=config.APP_VERSION
    )


@app.get("/models")
async def get_models():
    """
    Get available Groq models.
    
    Returns:
        dict: List of available models.
    """
    if not groq_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Groq service not initialized"
        )
    
    models = groq_service.get_available_models()
    return {"models": models}


@app.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """
    Generate chat completion using Groq API.
    
    Args:
        request (ChatRequest): Chat request with message and parameters.
        
    Returns:
        ChatResponse: Generated response from Groq.
        
    Raises:
        HTTPException: If service is unavailable or request fails.
    """
    if not groq_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Groq service not initialized"
        )
    
    try:
        response = await groq_service.chat_completion(request)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=response.response
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: FastAPI request object.
        exc: Exception that occurred.
        
    Returns:
        JSONResponse: Error response.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc) if config.DEBUG else "An unexpected error occurred"
        }
    )


def main():
    """
    Main function to run the FastAPI application.
    """
    uvicorn.run(
        "backend.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info"
    )


if __name__ == "__main__":
    main()
