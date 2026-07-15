import ast


def analyze_python_file(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        code = file.read()

    try:
        tree = ast.parse(code)

    except SyntaxError as e:

        return [
            {
                "file": file_path,
                "issue": "Syntax error",
                "severity": "high",
                "details": str(e)
            }
        ]

    issues = []

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

            # Check missing docstring
            if ast.get_docstring(node) is None:

                issues.append(
                    {
                        "file": file_path,
                        "function": node.name,
                        "issue": "Missing docstring",
                        "severity": "medium"
                    }
                )

            # Check too many parameters
            if len(node.args.args) > 5:

                issues.append(
                    {
                        "file": file_path,
                        "function": node.name,
                        "issue": "Too many function arguments",
                        "severity": "high"
                    }
                )

            # Check long functions
            if hasattr(node, "end_lineno"):

                function_length = (
                    node.end_lineno -
                    node.lineno
                )

                if function_length > 50:

                    issues.append(
                        {
                            "file": file_path,
                            "function": node.name,
                            "issue": "Function is too long",
                            "severity": "high"
                        }
                    )

    return issues