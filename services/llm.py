"""
services/llm.py

This module initializes and returns the LLM instance used
throughout the application.

For Hugging Face deployment, the OpenAI API key is provided
by the user through the Streamlit sidebar.
"""

import streamlit as st
from langchain_openai import ChatOpenAI
from config.settings import settings


class LLMService:
    """Returns an LLM instance using the user's API key."""

    @classmethod
    def get_llm(cls):

        # Get the API key entered by the user
        api_key = st.session_state.get("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "Please enter your OpenAI API Key in the sidebar."
            )

        return ChatOpenAI(
            api_key=api_key,
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
        )