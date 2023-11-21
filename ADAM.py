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
from keras.models import Model
from keras.layers import Input, LSTM, Dense
from datetime import date
import json
import matplotlib.pyplot as plt


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

batch_size = 64
epochs = 100 #оптимально 13
latent_dim = 256
num_samples = 10000

# Путь к файлу с тренировочными данными
data_path = 'dataset/dataset.json'

# Чтение данных из файла
input_texts = []
target_texts = []
input_characters = set()
target_characters = set()
with open(data_path, 'r', encoding='utf-8') as file:  
     data = json.load(file)
for i in range(len(data)):
     input_text = data[i]['Вопрос']
     target_text = data[i]['Ответ']
     input_texts.append(input_text)
     target_texts.append(target_text)
     for char in input_text:
          if char not in input_characters:
               input_characters.add(char)
     for char in target_text:
          if char not in target_characters:
               target_characters.add(char)

# Создание словаря символов
input_characters = sorted(list(input_characters))
target_characters = sorted(list(target_characters))
num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = max([len(txt) for txt in input_texts])
max_decoder_seq_length = max([len(txt) for txt in target_texts])
input_token_index = dict([(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict([(char, i) for i, char in enumerate(target_characters)])


# Инициализация нулевых массивов для хранения данных
encoder_input_data = np.zeros((len(input_texts), max_encoder_seq_length, num_encoder_tokens), dtype='float32')
decoder_input_data = np.zeros((len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype='float32')
decoder_target_data = np.zeros((len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype='float32')


# Заполнение массивов данными
for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
    for t, char in enumerate(input_text):
        encoder_input_data[i, t, input_token_index[char]] = 1.0
    for t, char in enumerate(target_text):
        decoder_input_data[i, t, target_token_index[char]] = 1.0
        if t > 0:
            decoder_target_data[i, t - 1, target_token_index[char]] = 1.0

# Определение модели
# Энкодер
encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder = LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]

decoder_inputs = Input(shape=(None, num_decoder_tokens))
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = Dense(num_decoder_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Объединение моделей
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Компиляция модели
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

# Тренировка модели
model.fit([encoder_input_data, decoder_input_data], 
          decoder_target_data, 
          batch_size=batch_size, 
          epochs=epochs, 
          validation_split=0.2)

model.save('model/Eva1.0.h5')
