from google import genai
import os


def generate_ai_review(prompt):

    try:
        print("\n========== GEMINI DEBUG START ==========")

        # Check API key
        api_key = os.getenv("GEMINI_API_KEY")

        print("API Key Present:", bool(api_key))

        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing")

        # Initialize client
        client = genai.Client(
            api_key=api_key
        )

        model = os.getenv(
            "LLM_MODEL",
            "gemini-flash-latest"
        )

        print("Using Model:", model)

        # Show prompt information
        print("\n----- PROMPT -----")
        print(prompt)
        print("----- END PROMPT -----\n")

        # Gemini call
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        print("\n----- RAW GEMINI RESPONSE -----")
        print(response)
        print("----- END RAW RESPONSE -----\n")

        # Extract text safely
        review_text = response.text

        print("----- RESPONSE TEXT -----")
        print(review_text)
        print("----- END RESPONSE TEXT -----\n")

        print("========== GEMINI DEBUG END ==========\n")

        return review_text


    except Exception as e:

        print("\n========== GEMINI ERROR ==========")
        print(type(e).__name__)
        print(str(e))
        print("========== END ERROR ==========\n")

        return f"AI Review generation failed: {str(e)}"
print(os.getcwd())
print(os.getenv("GEMINI_API_KEY"))