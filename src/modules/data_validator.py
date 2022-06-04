import PIL
from PIL import Image
from pathlib import Path

"""
    param:
        path: directory path
"""

def data_validator(path):
    path = Path(path).rglob("*.*")
    for img_path in path:
        try:
            img = Image.open(img_path)
        except PIL.UnidentifiedImageError:
            print(img_path)
            raise


