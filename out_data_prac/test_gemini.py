import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="Say OK in one word.",
)
print(interaction.output_text)