# feboun/utils / file_path.py
# Created by azat at 3.04.2023
from pathlib import Path


def handle_path(path: str) -> None:
    cwd = Path.cwd()
    data_dir = cwd / "data"
    if not data_dir.exists():
        data_dir.mkdir()
        print(f"Data dir: '{data_dir}' has been created.")
    else:
        print(f"The folder '{data_dir}' already exists, skipping creation.")
    print(f"Working from {cwd}")
