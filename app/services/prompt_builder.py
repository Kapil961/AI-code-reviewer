def build_review_prompt(review_context):

    project = review_context["project"]
    issues = review_context["issues"]

    issue_text = ""

    for issue in issues:
        issue_text += (
            f"- File: {issue['file']}\n"
            f"  Function: {issue.get('function', 'N/A')}\n"
            f"  Issue: {issue['issue']}\n"
            f"  Severity: {issue['severity']}\n\n"
        )

    prompt = f"""
You are an expert Python code reviewer.

Analyze the following repository.

Repository Summary
------------------
Total Files: {project['total_files']}
Total Classes: {project['total_classes']}
Total Functions: {project['total_functions']}

Detected Issues
---------------
{issue_text}

Write a professional review in this format:

## Overall Score
Give a score out of 10.

## Strengths

## Weaknesses

## Code Quality Suggestions

## Security Suggestions

## Final Verdict

Keep the response concise (250-350 words).
"""

    return prompt