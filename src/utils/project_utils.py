from pathlib import Path


def return_project_root() -> Path:
    return Path(__file__).parents[2]
