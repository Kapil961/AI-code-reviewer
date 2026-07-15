from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

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

from app.services.report_generator import (
    generate_report
)


router = APIRouter(
    prefix="/review",
    tags=["Code Review"]
)


UPLOAD_FOLDER = "uploads"


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@router.post("/upload")
async def upload_project(file: UploadFile = File(...)):


    # -------------------------
    # Validate ZIP file
    # -------------------------

    if not file.filename.endswith(".zip"):

        raise HTTPException(
            status_code=400,
            detail="Only ZIP files are allowed."
        )


    # -------------------------
    # Save uploaded ZIP
    # -------------------------

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )


    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    # -------------------------
    # Extract Repository
    # -------------------------

    project_path = extract_repository(
        file_path
    )


    # -------------------------
    # Find Python Files
    # -------------------------

    python_files = get_python_files(
        project_path
    )


    # -------------------------
    # AST Analysis
    # -------------------------

    ast_results = []


    for python_file in python_files:

        result = parse_python_file(
            python_file
        )

        ast_results.append(
            result
        )


    # -------------------------
    # Static Analysis
    # -------------------------

    code_issues = []


    for python_file in python_files:

        issues = analyze_python_file(
            python_file
        )

        code_issues.extend(
            issues
        )


    # -------------------------
    # Generate Review Context
    # -------------------------

    review_context = generate_review_context(
        project_path,
        ast_results,
        code_issues
    )


    # -------------------------
    # Build AI Prompt
    # -------------------------

    review_prompt = build_review_prompt(
        review_context
    )


    # -------------------------
    # Generate AI Review
    # -------------------------

    try:

        ai_review = generate_ai_review(
            review_prompt
        )


    except Exception as e:

        ai_review = (
            f"AI Review generation failed: {str(e)}"
        )


    # -------------------------
    # Save Markdown Report
    # -------------------------

    report_path = generate_report(
        project_path,
        ai_review
    )


    # -------------------------
    # API Response
    # -------------------------

    return {

        "message": "Project analyzed successfully",

        "project_name": os.path.basename(
            project_path
        ),

        "files_analyzed": len(
            python_files
        ),

        "issues_found": len(
            code_issues
        ),

        "report_path": report_path,

        "download_url":
            f"/review/report/{os.path.basename(report_path)}",

        "ai_review": ai_review

    }



# -------------------------
# Download AI Review Report
# -------------------------

@router.get("/report/{filename}")
async def download_report(filename: str):


    report_path = os.path.join(
        "reports",
        filename
    )


    if not os.path.exists(report_path):

        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )


    return FileResponse(
        path=report_path,
        filename=filename,
        media_type="text/markdown"
    )