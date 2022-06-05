"""
Import statements
"""
import digit
import data_processing

from tensorflow import keras
digit_model = keras.models.load_model("/home/azureuser/DataAnalyzer/src/digit_model.h5")

# To acces the model

"""
load the model
"""

#call function predict_model with image path and the model

# in the path we must specify (cat/dog,letter,digit)

# you have to provide the path here

img_path = "/home/azureuser/digit_data/testing/0/7410.png"


def perfom_prediction(img_path,mode):
    if(mode=="digit"):
        return data_processing.predict_model(img_path,digit_model)
    elif(mode=="letter"):
        return data_processing.predict_model(img_path, "you have to replace with the letter model")
    elif(mode=="catvsdog"):
        return data_processing.predict_model(img_path, "you have to replace with the cat/dog model")
perfom_prediction(img_path,"digit")