import streamlit as st
import os
import shutil

from app.services.file_loader import (
    extract_repository,
    get_python_files
)

from app.services.ast_parser import (
    parse_python_file
)

from app.services.analyzer import (
    analyze_python_file
)

from app.services.review_engine import (
    generate_review_context
)

from app.services.prompt_builder import (
    build_review_prompt
)

from app.services.llm_reviewer import (
    generate_ai_review
)


st.title("🤖 AI Code Reviewer")

st.write(
    "Upload your Python repository ZIP file "
    "to generate AI-powered code review."
)


uploaded_file = st.file_uploader(
    "Upload ZIP file",
    type=["zip"]
)


if uploaded_file:

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    zip_path = os.path.join(
        "uploads",
        uploaded_file.name
    )


    with open(zip_path, "wb") as f:
        f.write(
            uploaded_file.getbuffer()
        )


    st.success(
        "ZIP uploaded successfully"
    )


    if st.button("Generate Review"):

        with st.spinner(
            "Analyzing repository..."
        ):

            # Extract repository
            project_path = extract_repository(
                zip_path
            )


            # Find python files
            python_files = get_python_files(
                project_path
            )


            # AST Analysis
            ast_results = []

            for file in python_files:

                result = parse_python_file(
                    file
                )

                ast_results.append(result)


            # Static Analysis
            issues = []

            for file in python_files:

                result = analyze_python_file(
                    file
                )

                issues.extend(result)


            # Review context
            context = generate_review_context(
                project_path,
                ast_results,
                issues
            )


            # Prompt
            prompt = build_review_prompt(
                context
            )


            # Gemini
            ai_review = generate_ai_review(
                prompt
            )


        st.subheader(
            "📊 Analysis Summary"
        )

        st.write(
            f"Files analyzed: {len(python_files)}"
        )

        st.write(
            f"Issues found: {len(issues)}"
        )


        st.subheader(
            "🧠 AI Code Review"
        )


        st.markdown(
            ai_review
        )