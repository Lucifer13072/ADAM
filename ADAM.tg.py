from __future__ import absolute_import, division, print_function, unicode_literals
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import matplotlib.pyplot as plt
import tensorflow
from tensorflow import keras
from keras import layers
import collections
import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing import sequence
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib import pylab
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf



data = pd.read_csv('Models/dataset.csv')
np.random.seed(42)
max_features = 5000
maxlen = 80

model = keras.Sequential()

x = data['Вопрос']
y = data['Ответ']

tokenizer = keras.preprocessing.text.Tokenizer(num_words = max_features)
tokenizer.fit_on_texts(x + y)
sequences = tokenizer.texts_to_sequences(x)
y_sequences = tokenizer.texts_to_sequences(y)
x = pad_sequences(sequences, maxlen = maxlen)
y = pad_sequences(y_sequences, maxlen = maxlen)


x_train = train_test_split(x, test_size=0.2, random_state=42)
x_test = train_test_split(x, test_size=0.2, random_state=42)
y_train = train_test_split(y, test_size=0.2, random_state=42)
y_test = train_test_split(y, test_size=0.2, random_state=42)
 
 
 
model.add(layers.Embedding(input_dim=1500, output_dim=64))
model.add(layers.LSTM(428, dropout = 0.2))
model.add(layers.Dense(120, activation='relu'))
model.add(layers.Dense(520, activation='relu'))
model.add(layers.Dense(120, activation='softmax'))

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

x_test = np.stack(x_train, axis=0)
y_test = np.stack(y_train, axis=0)


model.fit(x_train, y_train, 
           batch_size = 64,
           epochs = 12,
           validation_data = (x_test, y_test),
           verbose = 1)

scores = model.evaluate(X_test, y_test, batch_size = 64)
print('Точность на тестовых данных: %f' % (scores[1] * 100))

plt.plot(scores, 0)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()