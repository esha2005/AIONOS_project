import os
import streamlit as st
from functools import lru_cache
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda
from config.settings import settings


GEMINI_MODEL_PRIORITY = [
    "gemini-3.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]

_5XX_EXCEPTIONS = (Exception,)


def _is_503_or_unavailable(exc: BaseException) -> bool:
    text = str(exc)
    markers = [
        "503", "UNAVAILABLE", "high demand", "try again later",
        "429", "RESOURCE_EXHAUSTED", "quota", "rate limit",
        "500", "INTERNAL", "504", "DEADLINE_EXCEEDED",
        "timeout",
    ]
    return any(m.lower() in text.lower() for m in markers)


@lru_cache(maxsize=16)
def _get_cached_llm(provider: str, key: str, model_name: str):
    if provider == "gemini":
        ordered_models = [model_name] + [
            m for m in GEMINI_MODEL_PRIORITY if m != model_name
        ]

        def _build_llm(m):
            return ChatGoogleGenerativeAI(
                google_api_key=key,
                model=m,
                temperature=settings.TEMPERATURE,
                max_retries=4,
                timeout=180,
            )

        llms = [_build_llm(m) for m in ordered_models]

        if len(llms) == 1:
            return llms[0]

        def _try_llms(input_data):
            last_exc = None
            for idx, llm in enumerate(llms):
                try:
                    return llm.invoke(input_data)
                except _5XX_EXCEPTIONS as exc:
                    last_exc = exc
                    if not _is_503_or_unavailable(exc):
                        raise
                    continue
            raise last_exc if last_exc is not None else RuntimeError("All LLM backends failed.")

        return RunnableLambda(_try_llms, name="GeminiMultiFallback")
    else:
        return ChatOpenAI(
            api_key=key,
            model=model_name,
            temperature=settings.TEMPERATURE,
            max_retries=4,
            timeout=180,
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
