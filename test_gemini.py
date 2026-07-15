from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="Explain what an AI code reviewer does in 3 lines."
)

print(response.text)