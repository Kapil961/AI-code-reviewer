from google import genai
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()


def generate_ai_review(prompt):

    try:

        print("\n========== GEMINI DEBUG START ==========")

        # Debug information
        print("Current Working Directory:", os.getcwd())

        api_key = os.getenv("GEMINI_API_KEY")
        print("API Key Present:", bool(api_key))

        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing")

        model = os.getenv(
            "LLM_MODEL",
            "gemini-flash-latest"
        )

        print("Using Model:", model)

        # Initialize Gemini Client
        client = genai.Client(
            api_key=api_key
        )

        print("\n----- PROMPT -----")
        print(prompt)
        print("----- END PROMPT -----\n")

        # Generate AI Review
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        print("\n----- RAW GEMINI RESPONSE -----")
        print(response)
        print("----- END RAW RESPONSE -----\n")

        review_text = response.text

        print("----- RESPONSE TEXT -----")
        print(review_text)
        print("----- END RESPONSE TEXT -----")

        print("\n========== GEMINI DEBUG END ==========\n")

        return review_text

    except Exception as e:

        print("\n========== GEMINI ERROR ==========")
        print("Error Type:", type(e).__name__)
        print("Error:", str(e))
        print("========== END ERROR ==========\n")

        return f"AI Review generation failed: {str(e)}"