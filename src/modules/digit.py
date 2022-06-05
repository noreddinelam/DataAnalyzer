# %% [markdown]
# # Handwritten Digit recognizer

# %% [markdown]
# The purpose of this model is to develop a  Convolutional Neural Network for recognizing handwritten digits
# 

# %% [markdown]
# ### Import statements

# %%
import tensorflow as tf
from keras.preprocessing import image
from keras.utils.vis_utils import plot_model
from tensorflow.python.keras.callbacks import ReduceLROnPlateau

import sys
sys.path.insert(1, "/home/azureuser/DataAnalyzer/src")

"""
Benchmark:
Bug : pour fixer le bug modifier le chemin /home/azureuser/DataAnalyzer/src/modules par /home/azureuser/DataAnalyzer/src : executer
 ensuite réexecuter avec /home/azureuser/DataAnalyzer/src/modules

"""
from modules.data_validator import *
from modules.data_processing import *


import string

from matplotlib import pyplot
from sklearn.metrics import confusion_matrix
import seaborn as sns

# %% [markdown]
# ## The data preparation
# 

# %%
sns.set(rc = {'figure.figsize':(15,15)})

# %% [markdown]
# ### Data Validation

# %% [markdown]
# Validate the dataset using the data_validator method

# %%

training_path = "/home/azureuser/digit_data/training"
testing_path =  "/home/azureuser/digit_data/testing"
validation_path =  "/home/azureuser/digit_data/validation"

for i in range(10):
    data_validator(training_path   + "/" + str(i))
    data_validator(testing_path    + "/" + str(i))
    data_validator(validation_path + "/"      + str(i))

# %% [markdown]
# ### Generate directory to read images from & Data augmentation

# %% [markdown]
# #### Normalization
# 
# To avoid overfitting we will alter our dataset.
# We chose :
# 
#     - Random rotation by 10° of some training image
#     - Brightness_range from 30 to 70 : The user will take picture so we will adapt our model
# 
#     -Shift image to make them not in the center
#         - Randomly shift images vertically
#         - Randomly shift images horizontally
# 

# %%
train_datagen = image.ImageDataGenerator(rescale=1.0/255.,rotation_range=10, zoom_range = 0.1, # Randomly zoom image
        width_shift_range=0.1,
        height_shift_range=0.1) 
test_datagen = image.ImageDataGenerator(rescale=1.0/255.,rotation_range=10, zoom_range = 0.1, # Randomly zoom image
        width_shift_range=0.1,
        height_shift_range=0.1)

validation_datagen = image.ImageDataGenerator(rescale=1.0/255.,rotation_range=10, zoom_range = 0.1, # Randomly zoom image
                        )


# %% [markdown]
# #### Generate and set directory to read images from with data augnemtation

# %%
#object of class ImageDataGenerator with the recale property
train_generator = train_datagen.flow_from_directory(training_path,batch_size=100,class_mode='sparse',target_size=(28, 28),color_mode="rgb", shuffle=True  )

test_generator = test_datagen.flow_from_directory(testing_path, batch_size=1,class_mode='sparse',target_size=(28, 28),color_mode="rgb", shuffle=False)

validation_generator = test_datagen.flow_from_directory(validation_path, batch_size=1,class_mode='sparse',target_size=(28, 28),color_mode="rgb", shuffle=True)


# %% [markdown]
# test_generator & train_generator are directory to read images from.
# Each subdirectory (digits directory) in this directory will be considered to contain images from one class.

# %%
print(test_generator.image_shape)
print(test_generator.classes)
print(train_generator.class_indices)

# %% [markdown]
# ## Data Visualisation

# %%
# plot first few images
for i in range(25):
	# define subplot
	pyplot.subplot(5, 5, i+1)
	# plot raw pixel data
	pyplot.imshow(train_generator[i][0][0], cmap=pyplot.get_cmap('gray'))
# show the figure
pyplot.show()

# %% [markdown]
# ## The CNN modeling and evaluation

# %% [markdown]
# ### Model

# %% [markdown]
# 
# Model : we have to avoid overfitting
# 
# Softmax :  Softmax takes a set of values, and effectively picks the biggest one, so, for example, if the output of the last layer looks like [0.1, 0.1, 0.05, 0.1, 9.5, 0.1, 0.05, 0.05, 0.05], it saves you from fishing through it looking for the biggest value, and turns it into [0,0,0,0,1,0,0,0,0] -- The goal is to save a lot of coding!
# activation layer : tf.keras.layers.Dense(10, activation=tf.nn.softmax)])
# 10 : because we have ten classes

# %%

digit_model = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28, 28,3)),
  tf.keras.layers.MaxPooling2D(2, 2),
  tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
  tf.keras.layers.MaxPooling2D(2, 2),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(256, activation='relu'),
  tf.keras.layers.Dense(10, activation='softmax')
])

# %% [markdown]
# ## Summarize Model
# 
# 
#     The layers and their order in the model.
# 
#     The output shape of each layer.
# 
#     The number of parameters (weights) in each layer.
# 
#     The total number of parameters (weights) in the model.

# %%
digit_model.summary()

# %% [markdown]
# #### Visualize a Deep Learning Neural Network Model in Keras

# %%
plot_model(digit_model, to_file='/home/azureuser/DataAnalyzer/src/benchmark/letters/model_plot_letter_1.png', show_shapes=True, show_layer_names=True)

# %% [markdown]
# #### compile the model
# Following the results got by  https://github.com/sanghvirajit/Feedforward_Neural_Network
# We make the choice of the RMSprop optimizer
# 

# %%
optimizer = tf.keras.optimizers.RMSprop(lr=0.001)

digit_model.compile(optimizer = optimizer, loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])

# %% [markdown]
# #### Train the model

# %% [markdown]
# Reduce learning rate when a metric has stopped improving,we will gain in time while fitting the model by converging faster to the global minimum by decreasing the learning rate.
# Set a learning rate annealer. we chose to decrease by 75%

# %%
learning_rate_reduction = ReduceLROnPlateau(monitor='val_accuracy',
                                            patience=3, # number of epochs with no improvement after which learning rate will be reduced.
                                            verbose=1, #update messages
                                            factor=0.25, #new_lr = lr * factor`.
                                            min_lr=0.00001 # minimum learning rate
                                            )

# %% [markdown]
# ### Fit model

# %%
history = digit_model.fit(train_generator, epochs=5, 
        validation_data=validation_generator,  callbacks=[learning_rate_reduction])

# %% [markdown]
# ## plot  curves

# %%

pyplot.title('Learning Curves')
pyplot.xlabel('Epoch')
pyplot.ylabel('Cross Entropy')
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='val')
pyplot.legend()
pyplot.show()

# %%
pyplot.title('Accuracy Curves')
pyplot.xlabel('Epoch')
pyplot.ylabel('Accuray')
pyplot.plot(history.history['accuracy'], label='Accuracy')
pyplot.plot(history.history['val_accuracy'], label='Val_Accuracy')
pyplot.legend()
pyplot.show()


# %% [markdown]
# ## Confusion matrix

# %%

test_generator.reset()
pred_list=[ ] # will store the predicted classes here
true_list=[]
classes=list(test_generator.class_indices.keys()) # ordered lst of class names 
prediction = digit_model.predict(test_generator)
predictions = prediction.argmax(axis=1)
labels=test_generator.labels
for i, p in enumerate (prediction):
    index=np.argmax(p)
    pred_list.append(classes[index])
    true_list.append(classes[labels[i]])
y_pred=np.array(pred_list)
y_true=np.array(true_list)



# %%
sns.set(rc = {'figure.figsize':(15,15)})
cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm,annot=True, fmt='g', cmap='Blues')

# %% [markdown]
# ## Model Evaluation

# %%
##TODO

test_generator.reset()
# Evaluate on Validation data
scores = digit_model.evaluate(test_generator)
print("%s%s: %.2f%%" % ("evaluate ",digit_model.metrics_names[1], scores[1]*100))


# %%
predict_model("/home/azureuser/digit_data/testing/0/7410.png",digit_model)

# %%
predict_model("/home/azureuser/digit_data/testing/2/3627.png",digit_model)

# %%
predict_model("/home/azureuser/digit_data/validation_statique/1.png",digit_model)

# %%
predict_model("/home/azureuser/digit_data/validation_statique/my0.png",digit_model)


