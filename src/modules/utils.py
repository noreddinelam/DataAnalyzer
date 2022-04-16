import os
from pathlib import Path


def make_dir(path: str):
    if not os.path.exists(path):
        pathToCreate = Path(path)
        pathToCreate.mkdir(parents=True, exist_ok=True)
