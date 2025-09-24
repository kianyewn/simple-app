"""
Streamlit frontend application for Simple Groq App.

This module contains the main Streamlit application interface.
"""

import os
import sys
import requests
import streamlit as st
from typing import List, Dict, Any

# Add the project root to Python path for imports
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.components.chat_interface import (
    render_chat_history,
    render_model_selector,
    render_chat_settings,
    render_loading_indicator,
    render_error_message,
    render_success_message
)

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


class StreamlitApp:
    """Main Streamlit application class."""
    
    def __init__(self):
        """Initialize the Streamlit application."""
        self.setup_page_config()
        self.initialize_session_state()
    
    def setup_page_config(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="Simple Groq App",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "available_models" not in st.session_state:
            st.session_state.available_models = ["mixtral-8x7b-32768"]
        
        if "backend_status" not in st.session_state:
            st.session_state.backend_status = "unknown"
    
    def check_backend_health(self) -> bool:
        """
        Check if the backend service is healthy.
        
        Returns:
            bool: True if backend is healthy, False otherwise.
        """
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                st.session_state.backend_status = "healthy"
                return True
            else:
                st.session_state.backend_status = "unhealthy"
                return False
        except Exception as e:
            st.session_state.backend_status = f"error: {str(e)}"
            return False
    
    def fetch_available_models(self) -> List[str]:
        """
        Fetch available models from the backend.
        
        Returns:
            List[str]: List of available model names.
        """
        try:
            response = requests.get(f"{BACKEND_URL}/models", timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", ["mixtral-8x7b-32768"])
                st.session_state.available_models = models
                return models
            else:
                return ["mixtral-8x7b-32768"]
        except Exception as e:
            st.warning(f"Could not fetch models: {str(e)}")
            return ["mixtral-8x7b-32768"]
    
    def send_chat_request(self, message: str, model: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send chat request to the backend.
        
        Args:
            message (str): User message.
            model (str): Selected model.
            settings (Dict[str, Any]): Chat settings.
            
        Returns:
            Dict[str, Any]: Response from the backend.
        """
        try:
            # Prepare chat history for the API
            history = []
            for msg in st.session_state.messages:
                if msg.get("role") in ["user", "assistant"]:
                    history.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Prepare request payload
            payload = {
                "message": message,
                "model": model,
                "max_tokens": settings["max_tokens"],
                "temperature": settings["temperature"],
                "history": history
            }
            
            # Send request to backend
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                error_detail = response.json().get("detail", "Unknown error")
                return {"error": f"API Error: {error_detail}"}
                
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def render_header(self):
        """Render the application header."""
        st.title("🤖 Simple Groq App")
        st.markdown("*Chat with AI using Groq's powerful language models*")
        
        # Backend status indicator
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.session_state.backend_status == "healthy":
                st.success("🟢 Backend Online")
            elif st.session_state.backend_status == "unhealthy":
                st.error("🔴 Backend Offline")
            else:
                st.warning("🟡 Backend Status Unknown")
        
        with col2:
            if st.button("🔄 Refresh Status"):
                with st.spinner("Checking backend..."):
                    self.check_backend_health()
                st.rerun()
    
    def render_main_interface(self):
        """Render the main chat interface."""
        # Check backend health on startup
        if st.session_state.backend_status == "unknown":
            with st.spinner("Connecting to backend..."):
                health_ok = self.check_backend_health()
                if health_ok:
                    self.fetch_available_models()
        
        # Chat settings sidebar
        settings = render_chat_settings()
        
        # Model selection
        with st.sidebar:
            st.header("🤖 Model Selection")
            if st.button("🔄 Refresh Models"):
                with st.spinner("Fetching models..."):
                    self.fetch_available_models()
            
            selected_model = render_model_selector(st.session_state.available_models)
        
        # Main chat area
        st.header("💬 Chat")
        
        # Chat history
        render_chat_history(st.session_state.messages)
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            if st.session_state.backend_status != "healthy":
                render_error_message("Backend is not available. Please check the connection.")
                return
            
            # Add user message to history
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Show user message immediately
            with st.chat_message("user"):
                st.write(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Generating response..."):
                    response = self.send_chat_request(prompt, selected_model, settings)
                
                if "error" in response:
                    error_msg = response["error"]
                    st.error(f"❌ {error_msg}")
                    # Add error to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Error: {error_msg}"
                    })
                else:
                    assistant_response = response.get("response", "No response generated.")
                    st.write(assistant_response)
                    
                    # Add assistant message to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_response
                    })
                    
                    # Show token usage info
                    tokens_used = response.get("tokens_used", 0)
                    if tokens_used > 0:
                        st.caption(f"Tokens used: {tokens_used}")
    
    def render_footer(self):
        """Render the application footer."""
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; color: #666;">
                <p>Built with ❤️ using Streamlit, FastAPI, and Groq</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def run(self):
        """Run the Streamlit application."""
        self.render_header()
        self.render_main_interface()
        self.render_footer()


def main():
    """Main function to run the Streamlit app."""
    app = StreamlitApp()
    app.run()


if __name__ == "__main__":
    main()
