def main():
    print("")

import PIL
from pathlib import Path
from PIL import UnidentifiedImageError
i=0
path = Path(r"C:\Users\idris\OneDrive\Bureau\Study\s6\DATA\kagglecatsanddogs_3367a\training\dog").rglob("*.jpg")
for img_p in path:
    try:
        img = PIL.Image.open(img_p)
    except PIL.UnidentifiedImageError:
        print(img_p)
