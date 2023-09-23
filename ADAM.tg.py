from __future__ import absolute_import, division, print_function, unicode_literals
import os
from tensorflow import keras
from keras import layers
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf

data = pd.read_csv('Models/dataset.csv')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
np.random.seed(42)
max_features = 1000
maxlen = 80

x = data['Вопрос']
y = data['Ответ']

tokenizer = keras.preprocessing.text.Tokenizer(num_words = max_features)
tokenizer.fit_on_texts(x + y)
sequences = tokenizer.texts_to_sequences(x)
y_sequences = tokenizer.texts_to_sequences(y)
x = pad_sequences(sequences, maxlen = maxlen)
y = pad_sequences(y_sequences, maxlen = maxlen)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = keras.Sequential()

model.add(layers.Embedding(input_dim = max_features, output_dim=64))
model.add(layers.LSTM(240, dropout = 0.2))
model.add(layers.Dense(120, activation='relu'))
model.add(layers.Dense(120, activation='softmax'))
tf.keras.layers.Dense(1, activation="sigmoid")
#Seq2Seq

model.compile(loss = 'sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

y_train = np.asarray(y_train).astype('float32').reshape((-1,1))
y_test = np.asarray(y_test).astype('float32').reshape((-1,1))
x_train = np.asarray(x_train).astype('float32').reshape((-1,1))
x_test = np.asarray(x_test).astype('float32').reshape((-1,1))

model.fit(x_train, y_train, 
           batch_size = 64,
           epochs = 12,
           validation_data = (x_test, y_test),
           verbose = 1)

scores = model.evaluate(x_test, y_test, batch_size = 64)
print('Точность на тестовых данных: %f' % (scores[1] * 100))