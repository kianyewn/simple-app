"""
Chat models for request and response validation.

This module defines Pydantic models for chat-related API endpoints.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Represents a single chat message."""
    
    role: str = Field(..., description="Role of the message sender (user, assistant, system)")
    content: str = Field(..., description="Content of the message", min_length=1)


class ChatRequest(BaseModel):
    """Request model for chat completion."""
    
    message: str = Field(..., description="User message to process", min_length=1, max_length=4000)
    model: str = Field(default="mixtral-8x7b-32768", description="Groq model to use")
    max_tokens: int = Field(default=1000, description="Maximum tokens in response", ge=1, le=4000)
    temperature: float = Field(default=0.7, description="Response randomness", ge=0.0, le=2.0)
    history: Optional[List[ChatMessage]] = Field(default=[], description="Previous chat messages")


class ChatResponse(BaseModel):
    """Response model for chat completion."""
    
    response: str = Field(..., description="Generated response from the model")
    model: str = Field(..., description="Model used for generation")
    tokens_used: int = Field(..., description="Number of tokens used in the response")
    success: bool = Field(..., description="Whether the request was successful")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(..., description="Health status")
    message: str = Field(..., description="Health check message")
    version: str = Field(..., description="Application version")
