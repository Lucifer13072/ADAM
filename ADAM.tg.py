from __future__ import absolute_import, division, print_function, unicode_literals
import os
import matplotlib.pyplot as plt
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
from itertools import zip_longest

data = pd.read_csv('Models/dataset.csv')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
np.random.seed(42)
max_features = 1000
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

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# aligned_lists = zip_longest(x_train, y_train, fillvalue='00')
# x_train, y_train = zip(*aligned_lists)

# aligned_lists = zip_longest(x_test, y_test, fillvalue='00')
# x_test, y_test = zip(*aligned_lists)

#ИЛИ

x_train = sequence.pad_sequences(x_train, maxlen = maxlen)
x_test = sequence.pad_sequences(x_test, maxlen = maxlen)

model.add(layers.Embedding(input_dim=1000, output_dim=64))
model.add(layers.LSTM(240, dropout = 0.2))
model.add(layers.Dense(120, activation='relu'))
model.add(layers.Dense(120, activation='softmax'))
#Seq2Seq

model.compile(loss = 'binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(x_train, y_train, 
           batch_size = 64,
           epochs = 12,
           validation_data = (x_test, y_test),
           verbose = 1)

# scores = model.evaluate(x_test, y_test, batch_size = 64)
# print('Точность на тестовых данных: %f' % (scores[1] * 100))
# plt.plot(scores, 0)
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.show()