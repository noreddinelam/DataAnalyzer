import PIL
from PIL import Image
from pathlib import Path

i=0
def data_validator(path):
    path = Path(path).rglob("*.*")
    for img_path in path:
        try:
            global i
            img = Image.open(img_path)
            print(img_path)
            print(i)
            i+=1
        except PIL.UnidentifiedImageError:
            print(img_path)
            raise


if __name__ == '__main__':
    """
    param:
        path: directory path
    """
    data_validator("/home/azureuser/data/training/cat")
