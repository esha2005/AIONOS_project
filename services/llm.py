import os
import streamlit as st
from functools import lru_cache
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings


@lru_cache(maxsize=16)
def _get_cached_llm(provider: str, key: str, model_name: str):
    if provider == "gemini":
        primary_llm = ChatGoogleGenerativeAI(
            google_api_key=key,
            model=model_name,
            temperature=settings.TEMPERATURE,
            max_retries=2,
            timeout=120,
        )

        fallback_candidates = [
            m for m in [
                "gemini-2.0-flash",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
            ]
            if m != model_name
        ]

        if fallback_candidates:
            fallback_llms = [
                ChatGoogleGenerativeAI(
                    google_api_key=key,
                    model=m,
                    temperature=settings.TEMPERATURE,
                    max_retries=2,
                    timeout=120,
                )
                for m in fallback_candidates[:2]
            ]
            return primary_llm.with_fallbacks(fallback_llms)
        return primary_llm
    else:
        return ChatOpenAI(
            api_key=key,
            model=model_name,
            temperature=settings.TEMPERATURE,
            max_retries=2,
            timeout=120,
        )


class LLMService:
    """Returns an LLM instance using user session or environment configuration."""

    @classmethod
    def get_llm(cls, provider: str = None, api_key: str = None):
        provider = provider or os.getenv("LLM_PROVIDER", "openai").lower()

        if provider == "gemini":
            session_key = None
            session_model = None
            try:
                if "st" in globals() and hasattr(st, "session_state"):
                    session_key = st.session_state.get("GOOGLE_API_KEY") or st.session_state.get("API_KEY") or st.session_state.get("OPENAI_API_KEY")
                    session_model = st.session_state.get("GEMINI_MODEL_NAME")
            except Exception:
                pass

            key = api_key or os.getenv("GOOGLE_API_KEY") or session_key

            if not key:
                raise ValueError("Please provide a valid Google Gemini API Key.")

            chosen_model = session_model or os.getenv("GEMINI_MODEL_NAME") or "gemini-2.0-flash"

            return _get_cached_llm("gemini", key, chosen_model)
        else:
            key = api_key or os.getenv("OPENAI_API_KEY")
            if not key and "st" in globals() and hasattr(st, "session_state"):
                key = st.session_state.get("OPENAI_API_KEY")

            if not key:
                raise ValueError("Please enter your OpenAI API Key.")

            return _get_cached_llm("openai", key, settings.MODEL_NAME)
