from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow
from tensorflow import keras
from keras import layers
import collections
import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing import sequence

np.random.seed(42)
max_features = 5000
maxlen = 80

model = keras.Sequential()

(X_train, y_train), (X_test, y_test) = DATASET.load_data(nb_words = max_features)
X_train = sequence.pad_sequences(X_train, maxlen = maxlen)
X_test = sequence.pad_sequences(X_test, maxlen = maxlen)

model.add(layers.Embedding(input_dim=1000, output_dim=64))
model.add(layers.LSTM(128))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, y_train, 
           batch_size = 64,
           nb_epoch = 12,
           validation_data = (X_test, y_test),
           verbose = 1)