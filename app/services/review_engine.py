def generate_review_context(
    project_path,
    ast_results,
    code_issues
):

    total_files = len(ast_results)

    total_functions = 0
    total_classes = 0

    for file in ast_results:

        total_functions += len(
            file.get("functions", [])
        )

        total_classes += len(
            file.get("classes", [])
        )

    context = {

        "project": {
            "path": project_path,
            "total_files": total_files,
            "total_functions": total_functions,
            "total_classes": total_classes
        },

        "issues": code_issues,

        "summary": {
            "issue_count": len(code_issues),
            "review_message":
                "Analyze this repository and provide code improvement suggestions."
        }

    }

    return context