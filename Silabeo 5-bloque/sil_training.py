# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:52:02 2021

@author: Wilfridovich
"""

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

def load_nparray(file_name):
    f = open(file_name,'rb')
    arr = np.load(f)
    f.close()
    
    return arr

#Prepare data
# Model / data parameters
num_classes = 5
input_shape = (6,)

# the data, split between train and test sets
x_train = load_nparray('syllabification_xtrain.np')
y_train = load_nparray('syllabification_ytrain.np')

print(np.sum(y_train[:,1]))

#MODEL
model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        layers.Dense(12, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(5, activation="softmax"),          
    ]
)

model.summary()

batch_size = 100
epochs = 4000

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1, class_weight = {0: 11.14, 1: 1.0, 2:1.90, 3:9.52, 4:208.0})

model_json = model.to_json()
with open("sil_model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("sil_weights.h5")

