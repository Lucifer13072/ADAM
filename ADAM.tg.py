from __future__ import absolute_import, division, print_function, unicode_literals
import os
from tensorflow import keras
from keras import layers
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from datetime import date

data = pd.read_csv('Models/dataset.csv')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
dt_now = date.today()
np.random.seed(42)
max_features = 1500
maxlen = 250

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
model.add(layers.LSTM(540, dropout = 0.2))
model.add(layers.Dense(540, activation='relu'))
model.add(layers.Dense(1540, activation='softmax'))
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
model.save(f'Out/Out_model_{dt_now}.h5')
print('Модель успешно сохранена!')

model.summary()

model_loaded = keras.models.load_model('Out/Out_model_2023-09-25.h5')

class NeuralNetwork(tf.keras.Model):
    def __init__(self, units):
        super().__init__()
        self.units = units
        self.model_layers = [layers.Dense(n, activation='relu') for n in self.units]
 
    def call(self, inputs):
        x = inputs
        for layer in self.model_layers:
            x = layer(x)
        return x

model = NeuralNetwork([128, 10])
y = model.predict(tf.expand_dims(x_test[0], axis=0))
model.save('out/16_model')
model_loaded = keras.models.load_model('out/16_model')
y = model_loaded.predict(tf.expand_dims(x_test[0], axis=0))

class NeuralNetworkLinear(tf.keras.Model):
    def __init__(self, units):
        super().__init__()
        self.units = units
        self.model_layers = [layers.Dense(n, activation='linear') for n in self.units]
 
    def call(self, inputs):
        x = inputs
        for layer in self.model_layers:
            x = layer(x)
        return x
    
model_loaded = keras.models.load_model('out/16_model', custom_objects={"NeuralNetwork": NeuralNetworkLinear})

def get_config(self):
        return {'units': self.units}
 
@classmethod
def from_config(cls, config):
        return cls(**config)

config = model.get_config()
model = NeuralNetwork([128, 10])
model2 = NeuralNetwork([128, 10])
y = model.predict(tf.expand_dims(x_test[0], axis=0))
y = model2.predict(tf.expand_dims(x_test[0], axis=0))
weights = model.get_weights()
model2.set_weights(weights)
y = model2.predict(tf.expand_dims(x_test[0], axis=0))
model.save_weights('out/model_weights')
model2.load_weights('out/model_weights')
model.save_weights('out/model_weights.h5')
model2.load_weights('out/model_weights.h5')
#model.predict