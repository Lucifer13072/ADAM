from __future__ import absolute_import, division, print_function, unicode_literals
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from keras import layers
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from datetime import date

data = pd.read_csv('Models/dataset.csv')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
dt_now = date.today()
np.random.seed(42)
max_features = 155000
maxlen = 350

x = data['Вопрос']
y = data['Ответ']

tokenizer = Tokenizer(num_words = max_features)
tokenizer.fit_on_texts(x + y)
sequences = tokenizer.texts_to_sequences(x)
y_sequences = tokenizer.texts_to_sequences(y)
x = pad_sequences(sequences, maxlen = maxlen)
y = pad_sequences(y_sequences, maxlen = maxlen)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = keras.Sequential()

model.add(layers.Embedding(max_features, 64, input_length=maxlen))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(64, 5, activation='relu'))
model.add(layers.MaxPooling1D(pool_size=4))
model.add(layers.LSTM(240))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(350, activation='softmax'))
tf.keras.layers.Dense(1, activation="sigmoid")

#Seq2Seq

model.compile(loss = 'categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(x_train, y_train, 
           batch_size = 64,
           epochs = 128,
           validation_data = (x_test, y_test))

max_seq_length = max(len(seq) for seq in x + y)
vocab_size = len(tokenizer.word_index) + 1
metadata = {
'tokenizer': tokenizer,
'max_seq_length': max_seq_length,
'vocab_size': vocab_size
}

model.summary()
scores = model.evaluate(x_test, y_test, batch_size = 64)
print('Точность на тестовых данных: %f' % (scores[1] * 100))
model.save(f'Out/Out_model_{dt_now}.h5')
np.save(f'Out/metadata_{dt_now}.npy', metadata)
print('Модель успешно сохранена!')