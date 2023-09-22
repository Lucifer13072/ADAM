from __future__ import absolute_import, division, print_function, unicode_literals
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

data = pd.read_csv('Models/dataset.csv')
np.random.seed(42)
max_features = 5000
maxlen = 80

model = keras.Sequential()

X = data['Вопрос']
y = data['Ответ']

tokenizer = keras.preprocessing.text.Tokenizer(num_words = max_features)
tokenizer.fit_on_texts(X+y)
sequences = tokenizer.texts_to_sequences(X)
y_sequences = tokenizer.texts_to_sequences(y)
X = pad_sequences(sequences, maxlen = maxlen)
y = pad_sequences(y_sequences, maxlen = maxlen)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model.add(layers.Embedding(input_dim=1500, output_dim=64))
model.add(layers.LSTM(128, dropout = 0.2))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

X_test = np.array(X_test)
y_test = np.array(y_test)

model.fit(X_train, y_train, 
           batch_size = 64,
           epochs = 50,
           validation_data = (X_test, y_test),
           verbose = 1)

scores = model.evaluate(X_test, y_test, batch_size = 64)
print('Точность на тестовых данных: %f' % (scores[1] * 100))

# plt.plot(scores, 0)
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.show()
print("Hello world")