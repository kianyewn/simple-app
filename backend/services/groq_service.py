"""
Groq API service integration.

This module handles communication with the Groq API for language model inference.
"""

import os
from typing import List, Dict, Any
from groq import Groq
from backend.models.chat_models import ChatMessage, ChatRequest, ChatResponse


class GroqService:
    """Service class for Groq API integration."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Groq service.
        
        Args:
            api_key (str, optional): Groq API key. If not provided, reads from environment.
        
        Raises:
            ValueError: If API key is not provided or found in environment.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable.")
        
        self.client = Groq(api_key=self.api_key)
    
    def _format_messages(self, request: ChatRequest) -> List[Dict[str, str]]:
        """
        Format chat messages for Groq API.
        
        Args:
            request (ChatRequest): Chat request with message and history.
            
        Returns:
            List[Dict[str, str]]: Formatted messages for Groq API.
        """
        messages = []
        
        # Add system message if available
        if request.history:
            for msg in request.history:
                if msg.role in ["system", "user", "assistant"]:
                    messages.append({"role": msg.role, "content": msg.content})
        
        # Add current user message
        messages.append({"role": "user", "content": request.message})
        
        return messages
    
    async def chat_completion(self, request: ChatRequest) -> ChatResponse:
        """
        Generate chat completion using Groq API.
        
        Args:
            request (ChatRequest): Chat request parameters.
            
        Returns:
            ChatResponse: Generated response from Groq.
            
        Raises:
            Exception: If API call fails or returns invalid response.
        """
        try:
            messages = self._format_messages(request)
            
            # Make API call to Groq
            completion = self.client.chat.completions.create(
                model=request.model,
                messages=messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                stream=False
            )
            
            # Extract response data
            response_content = completion.choices[0].message.content
            tokens_used = completion.usage.total_tokens if completion.usage else 0
            
            return ChatResponse(
                response=response_content,
                model=request.model,
                tokens_used=tokens_used,
                success=True
            )
            
        except Exception as e:
            # Log error (in production, use proper logging)
            print(f"Groq API error: {str(e)}")
            
            # Return error response
            return ChatResponse(
                response=f"Error generating response: {str(e)}",
                model=request.model,
                tokens_used=0,
                success=False
            )
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available Groq models.
        
        Returns:
            List[str]: List of available model names.
        """
        # Common Groq models (this could be fetched from API in production)
        return [
            "llama-3.1-8b-instant"
        ]
