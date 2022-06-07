from pyexpat import model

import imageio
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import string
import cv2
from tensorflow import keras

width = 28
height = 28
dim = (width, height)
alphabet_string = string.ascii_uppercase
alphabet_list = list(alphabet_string)

catvsdog_list = ["cat","dog"]

def resize(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite(img_path, resized)

def loadImage(path):
    return Image.open(path)

def image(image_path):
    image = plt.imread(image_path)
    image = image[:, :, 0]
    image_2 = np.copy(image)

    plt.hist(image_2.ravel(), bins=255)
    plt.imshow(image, cmap="gray")

    image = image > 0.37
    image = np.where(image, 0, 255)
    #modification des x premier et dernier pixel
    #fin de l'image
    image[:, image.shape[1]-150:] = 0
    #début de l'image
    image[:, :150] = 0
    imageio.imwrite("../api/images_captured/new_image.png", image)

    plt.imshow(image)
    plt.show()


def predict_model(img_path, model_name, model):
    # your images in an array
   
    img = loadImage(img_path)
    #img.show()
    
    #difirencier le model chat vs chien 150*150
    if(model_name == "digit" or model_name == "letter"):
        if( img.size != (28,28)):
            image(img_path)
            img = loadImage("../api/images_captured/new_image.png")
        img = img.resize((28, 28))
    
    if(model_name == "catvsdog"):
        img = loadImage("../api/images_captured/new_image.png")
        img = img.resize((150, 150))
    
    #img.show()
    img = np.array(img)
    if (len(img.shape) != 3):
        image_color = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        image_color = img

    print(image_color.shape)
    x = np.expand_dims(image_color, axis=0)
    classes = model.predict(x)
    print(classes)
    if (model_name == "digit" or model_name == "letter"):
        print(classes.argmax(1))
        return str(classes.argmax(1)[0])
    else:
        print("catvsdog")
        return str(classes[0][0])

#Load the model

digit_model = keras.models.load_model("../models/digit_model.h5")
letter_model = keras.models.load_model("../models/letter2_model.h5")
catvsdog_model = keras.models.load_model("../models/catvsdog_model.h5")

def perfom_prediction(img_path,mode):
    if(mode=="digit"):
        return predict_model(img_path, mode, digit_model)
    elif(mode=="letter"):
        return alphabet_list[int(predict_model(img_path, mode, letter_model))]
    elif(mode=="catvsdog"):
        return catvsdog_list[int(float(predict_model(img_path, mode, catvsdog_model)))]

if __name__ == '__main__':
    predict_model(r"C:\Users\idris\OneDrive\Bureau\Study\s6\DATA\Dataset1\letter data set\testing\Z\4.jpg", 'letter', letter_model)