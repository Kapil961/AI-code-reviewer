import ast


def parse_python_file(file_path):

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
        return {
            "file": file_path,
            "error": "Syntax error in file",
            "details": str(e)
        }

    result = {
        "file": file_path,
        "functions": [],
        "classes": [],
        "imports": [],
        "async_functions": []
    }

    for node in ast.walk(tree):

        # Extract functions
        if isinstance(node, ast.FunctionDef):

            arguments = []

            for arg in node.args.args:
                arguments.append(arg.arg)

            result["functions"].append(
                {
                    "name": node.name,
                    "arguments": arguments,
                    "line": node.lineno
                }
            )

        # Extract async functions
        elif isinstance(node, ast.AsyncFunctionDef):

            arguments = []

            for arg in node.args.args:
                arguments.append(arg.arg)

            result["async_functions"].append(
                {
                    "name": node.name,
                    "arguments": arguments,
                    "line": node.lineno
                }
            )

        # Extract classes
        elif isinstance(node, ast.ClassDef):

            result["classes"].append(
                {
                    "name": node.name,
                    "line": node.lineno
                }
            )

        # Extract imports
        elif isinstance(node, ast.Import):

            for name in node.names:

                result["imports"].append(
                    name.name
                )

        # Extract from imports
        elif isinstance(node, ast.ImportFrom):

            if node.module:

                result["imports"].append(
                    node.module
                )

    return result