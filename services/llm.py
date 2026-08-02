"""
services/llm.py

This module initializes and returns the LLM instance used
throughout the application.
"""

from langchain_openai import ChatOpenAI
from config.settings import settings


class LLMService:
    """Singleton wrapper around ChatOpenAI."""

    _llm = None

    @classmethod
    def get_llm(cls):
        if cls._llm is None:

            if not settings.OPENAI_API_KEY:
                raise ValueError(
                    "OPENAI_API_KEY not found. Please check your .env file."
                )

            cls._llm = ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=settings.MODEL_NAME,
                temperature=settings.TEMPERATURE,
            )

        return cls._llm