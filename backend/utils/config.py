"""
Configuration management utilities.

This module handles application configuration and environment variables.
"""

import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""
    
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "Simple Groq App")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server settings
    HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    
    # Groq API settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        origin.strip() 
        for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(",")
    ]
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate that all required configuration is present.
        
        Returns:
            bool: True if configuration is valid, False otherwise.
        """
        required_vars = ["GROQ_API_KEY"]
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"Missing required environment variables: {', '.join(missing_vars)}")
            return False
        
        return True


# Global configuration instance
config = Config()
