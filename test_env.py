from dotenv import load_dotenv
import os

load_dotenv()

print("API KEY:", os.getenv("OPENAI_API_KEY"))
print("MODEL:", os.getenv("MODEL_NAME"))