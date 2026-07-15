from app.services.llm_reviewer import generate_ai_review

prompt = """
You are a senior Python code reviewer.

Review this project.

Issues:
- Missing docstrings
- No logging
- Add unit tests

Give 5 suggestions.
"""

print(generate_ai_review(prompt))