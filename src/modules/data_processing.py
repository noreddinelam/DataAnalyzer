from PIL import Image as PImage
import numpy as np

import cv2

width = 28
height = 28
dim = (width, height)


def resize(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite(img_path, resized)


# resize("C:\\Users\\idris\\OneDrive\\IMAGES\\dola.png")

def invert_color(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    # TODO : black and white image or gray we will see if we need it or we use rgb


def loadImage(path):
    return PImage.open(path)


def black_and_white(img):
    pixels = img.load()
    pix = pixels[0, 0]
    f=0
    print(pix)
    for i in range(img.size[0]):  # for every pixel:
        for j in range(img.size[1]):
            for k in range(3):
                f += pixels[i, j][k] - pix[k]

            if f > 20 or f < -20:
                if (f!=0) : print(f)
                pixels[i, j] = (255, 255, 255)
            else:
                #white
                pixels[i, j] = (0, 0, 0)
            f=0

#TODO : make the white thicker


def evaluate_digits_model(img_path,model):
    # your images in an array
    img = loadImage(img_path)
    img.show()
    black_and_white(img)
    img = img.resize((28, 28))
    img.show()
    img = np.array(img)
    if (len(img.shape) != 3):
        image_color = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        image_color = img

    print(image_color.shape)
    x = np.expand_dims(image_color, axis=0)
    classes = model.predict(x)
    max_value = max(classes)
    max_index = classes.index(max_value)
    print(max_index)


if __name__ == '__main__':
    "nothing to run"
    # evaluate_digits_model("/home/azureuser/DataAnalyzer/digit_data/testing/0/3.png")
    # evaluate_digits_model("/home/azureuser/DataAnalyzer/digit_data/my0_1.png")