import os
import shutil
import zipfile


EXTRACT_FOLDER = "extracted"


def extract_repository(zip_path):

    project_name = os.path.splitext(
        os.path.basename(zip_path)
    )[0]

    extract_path = os.path.join(
        EXTRACT_FOLDER,
        project_name
    )

    os.makedirs(
        EXTRACT_FOLDER,
        exist_ok=True
    )

    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)

    os.makedirs(
        extract_path,
        exist_ok=True
    )

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(
            extract_path
        )

    return extract_path


def get_python_files(project_path):

    python_files = []

    ignored_directories = {
        "__pycache__",
        ".git",
        ".venv",
        "venv",
        "env",
        "node_modules"
    }

    for root, directories, files in os.walk(project_path):

        directories[:] = [
            directory
            for directory in directories
            if directory not in ignored_directories
        ]

        for file in files:

            if file.endswith(".py"):

                python_files.append(
                    os.path.join(root, file)
                )

    return python_files