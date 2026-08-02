import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    """Application configuration."""

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0))

    APP_NAME = os.getenv(
        "APP_NAME",
        "AI HR Recruitment Assistant"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"


settings = Settings()