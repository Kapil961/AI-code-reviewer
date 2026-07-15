import os
from datetime import datetime


REPORT_FOLDER = "reports"

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


def generate_report(project_path, ai_review):

    project_name = os.path.basename(
        project_path
    )

    report_name = f"{project_name}_review.md"

    report_path = os.path.join(
        REPORT_FOLDER,
        report_name
    )


    report_content = f"""
# AI Code Review Report

## Project

{project_name}


## Generated At

{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


## AI Review

{ai_review}

"""


    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            report_content
        )


    return report_path