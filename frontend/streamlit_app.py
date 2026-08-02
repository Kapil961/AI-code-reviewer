import streamlit as st
import requests

# ----------------------------
# Backend URL
# ----------------------------
BACKEND_URL = "https://ai-code-reviewer-k023.onrender.com"

# ----------------------------
# Page
# ----------------------------
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Code Reviewer")

st.write(
    "Upload your Python repository ZIP file to generate an AI-powered code review."
)

# ----------------------------
# Upload ZIP
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload ZIP File",
    type=["zip"]
)

# ----------------------------
# Generate Review
# ----------------------------
if uploaded_file is not None:

    st.success("✅ ZIP uploaded successfully")

    if st.button("Generate Review"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/zip"
            )
        }

        try:

            with st.spinner("Analyzing repository... This may take a few minutes."):

                response = requests.post(
                    f"{BACKEND_URL}/review/upload",
                    files=files,
                    timeout=300
                )

            if response.status_code == 200:

                data = response.json()

                st.success(data["message"])

                st.subheader("📊 Analysis Summary")

                st.write(f"**Project:** {data['project_name']}")
                st.write(f"**Files Analyzed:** {data['files_analyzed']}")
                st.write(f"**Issues Found:** {data['issues_found']}")

                st.subheader("🧠 AI Code Review")

                st.markdown(data["ai_review"])

                report_url = BACKEND_URL + data["download_url"]

                st.markdown(
                    f"### 📄 [Download Markdown Report]({report_url})"
                )

            else:

                st.error(f"Backend Error ({response.status_code})")
                st.code(response.text)

        except requests.exceptions.Timeout:

            st.error(
                "⏰ Request timed out. The backend is taking too long to respond."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Could not connect to the backend.\n\n"
                "Please check that your Render backend is running."
            )

        except Exception as e:

            st.error(f"Unexpected Error:\n{e}")