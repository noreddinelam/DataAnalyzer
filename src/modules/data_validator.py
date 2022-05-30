import PIL
from PIL import Image
from pathlib import Path
training_path = "C:\\Users\\idris\\OneDrive\\Bureau\\Study\\s6\\DATA\\digtis\\mnist_png\\training\\"
testing_path =  "C:\\Users\\idris\\OneDrive\\Bureau\\Study\\s6\\DATA\\digtis\\mnist_png\\testing\\"

def data_validator(path):
    path = Path(path).rglob("*.*")
    for img_path in path:
        try:
            img = Image.open(img_path)
        except PIL.UnidentifiedImageError:
            print(img_path)
            raise


            

if __name__ == '__main__':
    """
    param:
        path: directory path
    """

