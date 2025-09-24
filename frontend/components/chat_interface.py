"""
Chat interface components for Streamlit frontend.

This module contains UI components for the chat interface.
"""

import streamlit as st
from typing import List, Dict, Any


def render_chat_message(message: Dict[str, Any], is_user: bool = True):
    """
    Render a single chat message.
    
    Args:
        message (Dict[str, Any]): Message data containing content and metadata.
        is_user (bool): Whether the message is from the user or assistant.
    """
    if is_user:
        with st.container():
            st.markdown(
                f"""
                <div style="
                    background-color: #e3f2fd;
                    padding: 10px;
                    border-radius: 10px;
                    margin: 10px 0;
                    text-align: right;
                ">
                    <strong>You:</strong> {message['content']}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        with st.container():
            st.markdown(
                f"""
                <div style="
                    background-color: #f5f5f5;
                    padding: 10px;
                    border-radius: 10px;
                    margin: 10px 0;
                ">
                    <strong>Assistant:</strong> {message['content']}
                </div>
                """,
                unsafe_allow_html=True
            )


def render_chat_history(messages: List[Dict[str, Any]]):
    """
    Render the entire chat history.
    
    Args:
        messages (List[Dict[str, Any]]): List of chat messages.
    """
    if not messages:
        st.info("💬 Start a conversation by typing a message below!")
        return
    
    # Create a container for chat messages
    chat_container = st.container()
    
    with chat_container:
        for message in messages:
            is_user = message.get("role") == "user"
            render_chat_message(message, is_user)


def render_model_selector(available_models: List[str], default_model: str = "mixtral-8x7b-32768"):
    """
    Render model selection dropdown.
    
    Args:
        available_models (List[str]): List of available model names.
        default_model (str): Default model to select.
        
    Returns:
        str: Selected model name.
    """
    if not available_models:
        available_models = [default_model]
    
    selected_model = st.selectbox(
        "🤖 Select AI Model:",
        available_models,
        index=0 if default_model not in available_models else available_models.index(default_model),
        help="Choose the AI model for generating responses"
    )
    
    return selected_model


def render_chat_settings():
    """
    Render chat settings in sidebar.
    
    Returns:
        Dict[str, Any]: Chat settings configuration.
    """
    with st.sidebar:
        st.header("⚙️ Chat Settings")
        
        # Temperature setting
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Controls randomness in responses. Lower values = more focused, Higher values = more creative"
        )
        
        # Max tokens setting
        max_tokens = st.slider(
            "Max Tokens",
            min_value=50,
            max_value=4000,
            value=1000,
            step=50,
            help="Maximum length of the response"
        )
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.rerun()
        
        return {
            "temperature": temperature,
            "max_tokens": max_tokens
        }


def render_loading_indicator():
    """Render loading indicator for API calls."""
    with st.spinner("🤔 Thinking..."):
        st.empty()


def render_error_message(error: str):
    """
    Render error message.
    
    Args:
        error (str): Error message to display.
    """
    st.error(f"❌ Error: {error}")


def render_success_message(message: str):
    """
    Render success message.
    
    Args:
        message (str): Success message to display.
    """
    st.success(f"✅ {message}")
