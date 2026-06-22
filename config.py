import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

LLM_MODEL = "llama-3.3-70b-versatile"

LANGUAGE_INSTRUCTION = {
    "english": "Respond in English only.",
    "roman_urdu": "Respond in Roman Urdu only (Urdu words written in English letters). For example: 'Yeh market bohat acha hai aur growth potential zabardast hai.'"
}