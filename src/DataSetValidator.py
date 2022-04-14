import PIL
from pathlib import Path


def data_validator(path):
    path = Path(path).rglob("*.*")
    for img_path in path:
        try:
            img = PIL.Image.open(img_path)
            print(img_path)
        except PIL.UnidentifiedImageError:
            print(img_path)
            raise


if __name__ == '__main__':
    """
    param:
        path: directory path
    """
    data_validator(r"C:\Users\idris\OneDrive\Bureau\Study\s6\DataAnalyzer\src\dataset\images\cats")
