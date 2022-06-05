import tensorflow as tf
import numpy as np
from tensorflow import keras

#model : réseau de neurones entrainé
# model basic de DNN
# single layer with single neurone units=1, input=1, output=1

model = tf.keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])

model.compile(optimizer='sgd', loss='mean_squared_error',metrics=['acc'])

xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)

ys = np.array([-3.0, -1.0, 1.0, 3.0, 5.0, 7.0], dtype=float)

xTest = np.array([5.0, 3.0, -1.0], dtype=float)
yTest = np.array([9.0, 5.0, -3.0], dtype=float)

# vu la simpliciter du probléme epochs=1000 reste une valeur exécutable par nos ordinateur
model.fit(xs, ys, epochs=1000)
model.evaluate(xTest,yTest)
# le modèle n'est pas précis à 100%, mais il est proche ; il n'est pas sûr que le résultat soit 19
print(f'prediction {model.predict([10.0])}')
