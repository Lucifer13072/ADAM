from __future__ import absolute_import, division, print_function, unicode_literals
import os
import numpy as np
import pandas as pd
import tensorflow as tf
import configparser
from tensorflow import keras as ker
from keras import layers
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from datetime import date
import json
import matplotlib.pyplot as plt


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


x = []
y = []
with open('dataset/dataset.json', 'r', encoding='utf-8' ) as j:
     data = json.loads(j.read())

for i in range(len(data)):
     x.append(data[i]['Вопрос'])
for i in range(len(data)):
     y.append(data[i]['Ответ'])

tokenizer = Tokenizer(num_words = 155000)
tokenizer.fit_on_texts(x + y)
sequences = tokenizer.texts_to_sequences(x)
y_sequences = tokenizer.texts_to_sequences(y)
x = pad_sequences(sequences, maxlen = 500)
y = pad_sequences(y_sequences, maxlen = 500)


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = ker.Sequential()

model.add(layers.Embedding(155000, 64, input_length=500))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(64, 5, activation='relu'))
model.add(layers.MaxPooling1D(pool_size=4))
model.add(layers.Dense(500, activation='relu')) 
model.add(layers.Dense(350, activation='relu'))  
model.add(layers.LSTM(400))  
model.add(layers.Dense(350, activation='relu'))  
model.add(layers.Dense(500, activation='softmax'))  

model.compile(loss = 'categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(x_train, y_train, 
           batch_size = 64,
           epochs = 6,
           validation_data = (x_test, y_test))


max_seq_length = max(len(seq) for seq in x + y)
vocab_size = len(tokenizer.word_index) + 1
metadata = {
'tokenizer': tokenizer,
'max_seq_length': max_seq_length,
'vocab_size': vocab_size
}

scores = model.evaluate(x_test, y_test, batch_size = 64)
print('Точность на тестовых данных: %f' % (scores[1] * 100))
model.save(f'Out/model.h5')
np.save(f'Out/metadata.npy', metadata)
print('Модель успешно сохранена!')

