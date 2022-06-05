from pyexpat import model
from PIL import Image as PImage
import numpy as np
import cv2

from tensorflow import keras

width = 28
height = 28
dim = (width, height)


def resize(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite(img_path, resized)



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

            if f > 50 or f < -50:
                if (f!=0) : print(f)
                pixels[i, j] = (255, 255, 255)
            else:
                #white
                pixels[i, j] = (0, 0, 0)
            f=0

def predict_model(img_path,model):
    # your images in an array
   
    img = loadImage(img_path)
    img.show()
    
    #difirencier le model chat vs chien 150*150
    if("digit" in img_path or "letter" in img_path):
        if( img.size != (28,28)):
            black_and_white(img)
        img = img.resize((28, 28))
    
    if("cat" in img_path or "dog" in img_path):
        img = img.resize((150, 150))
    
    img.show()
    img = np.array(img)
    if (len(img.shape) != 3):
        image_color = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        image_color = img

    print(image_color.shape)
    x = np.expand_dims(image_color, axis=0)
    classes = model.predict(x)
    print(classes)
    print(classes.argmax(1))
    #max_value = max(classes[0])
    #print(max_value)
    #max_index = np.where(classes[0] == max_value)
    #print(max_index[0][0])
    
    return classes.argmax(1)[0]

#Load the model

"""

"""
digit_model = keras.models.load_model("/home/azureuser/DataAnalyzer/src/digit_model.h5")




def perfom_prediction(img_path,mode):
    if(mode=="digit"):
        return predict_model(img_path,digit_model)
    elif(mode=="letter"):
        return predict_model(img_path, "you have to replace with the letter model")
    elif(mode=="catvsdog"):
        return predict_model(img_path, "you have to replace with the cat/dog model")



if __name__ == '__main__':
    #Run test
    img_path = "/home/azureuser/digit_data/testing/0/7410.png"
    perfom_prediction(img_path,"digit")
