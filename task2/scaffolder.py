import os
import shutil
from pathlib import Path

class NetworkError(Exception):
    pass

def download_gitignore(target_path: Path):
    # simulated request.get(...)
    raise NetworkError("Connection timeout while fetching .gitignore")

def create_project_structure(project_name: str):
    root = Path(project_name)
    
    print(f"Creating project '{project_name}'...")

    if root.exists():
        print(f"Error: Directory {project_name} already exists.")
        return
    root.mkdir()
    print(f"-> Created directory: {root}")

    src = root / "src"
    src.mkdir()
    print(f"-> Created directory: {src}")

    main_file = src / "main.py"
    main_file.write_text("print('Hello World')")
    print(f"-> Created file: {main_file}")

    try:
        print("-> Downloading .gitignore...")
        download_gitignore(root / ".gitignore")
    except NetworkError as e:
        print(f"CRITICAL ERROR: {e}")
        print("Aborting...")
        # PROBLEM: Script terminates but 'src' and 'main.py' stays.
        raise

if __name__ == "__main__":
    try:
        create_project_structure("my_new_app")
    except Exception:
        print("\nFailed. Check your directory - it's probably messy now.")