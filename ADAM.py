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

import tensorflow as tf
import numpy as np
import json

# Загрузка датасета из файла
with open('dataset/dataset.json', 'r') as file:
    dataset = json.load(file)

# Создание словарей для преобразования текста в числовой формат
input_texts = []
target_texts = []
input_characters = set()
target_characters = set()

for data in dataset:
    input_text = data['Вопрос']
    target_text = data['Ответ']
    input_texts.append(input_text)
    target_texts.append(target_text)
    for char in input_text:
        if char not in input_characters:
            input_characters.add(char)
    for char in target_text:
        if char not in target_characters:
            target_characters.add(char)

input_characters = sorted(list(input_characters))
target_characters = sorted(list(target_characters))
num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = max([len(txt) for txt in input_texts])
max_decoder_seq_length = max([len(txt) for txt in target_texts])

input_token_index = dict([(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict([(char, i) for i, char in enumerate(target_characters)])

# Создание и подготовка тренировочных данных
encoder_input_data = np.zeros(
    (len(input_texts), max_encoder_seq_length, num_encoder_tokens), dtype='float32')
decoder_input_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype='float32')
decoder_target_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype='float32')

for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
    for t, char in enumerate(input_text):
        encoder_input_data[i, t, input_token_index[char]] = 1.0
    for t, char in enumerate(target_text):
        decoder_input_data[i, t, target_token_index[char]] = 1.0
        if t > 0:
            decoder_target_data[i, t - 1, target_token_index[char]] = 1.0

# Определение параметров модели
latent_dim = 256

# Определение модели
encoder_inputs = tf.keras.Input(shape=(None, num_encoder_tokens))
encoder = tf.keras.layers.LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]

decoder_inputs = tf.keras.Input(shape=(None, num_decoder_tokens))
decoder_lstm = tf.keras.layers.LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = tf.keras.layers.Dense(num_decoder_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

model = tf.keras.Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Компиляция и обучение модели
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
          batch_size=64,
          epochs=50,
          validation_split=0.2)

# Сохранение модели
model.save('EVA_model.h5')


encoder_model = tf.keras.Model(encoder_inputs, encoder_states)

# Входы для модели декодера
decoder_state_input_h = tf.keras.layers.Input(shape=(latent_dim,))
decoder_state_input_c = tf.keras.layers.Input(shape=(latent_dim,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)

# Создаем модель декодера
decoder_model = tf.keras.Model([decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)

def decode_sequence(input_seq):
     # Кодируем входное сообщение в вектор состояний
     states_value = encoder_model.predict(input_seq)

     # Заполняем вектор декодера символом начала последовательности
     target_seq = np.zeros((1, 1, num_decoder_tokens))
     target_seq[0, 0, target_token_index['\t']] = 1.

     # Цикл по последовательности
     stop_condition = False
     decoded_sentence = ''
     target_token_index = dict(
          [(char, i) for i, char in enumerate(target_characters)]
     )

# Создание обратного словаря для перевода численных индексы в символы
     reverse_target_char_index = dict(
          (i, char) for char, i in target_token_index.items()
     )
     while not stop_condition:
          output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

          # Выбираем следующий символ
          sampled_token_index = np.argmax(output_tokens[0, -1, :])
          sampled_char = reverse_target_char_index[sampled_token_index]
          decoded_sentence += sampled_char

          # Если последовательность достигла максимальной длины или найден символ конца предложений
          if (sampled_char == '\n' or len(decoded_sentence) > max_decoder_seq_length):
               stop_condition = True

          # Обновляем входное сообщение декодера на следующий цикл
          target_seq = np.zeros((1, 1, num_decoder_tokens))
          target_seq[0, 0, sampled_token_index] = 1.

          # Обновляем состояния
          states_value = [h, c]

     return decoded_sentence

def chat(input_text):
     # Преобразуем входной текст в формат, подходящий для модели
     input_seq = np.zeros((1, max_encoder_seq_length, num_encoder_tokens), dtype="float32")
     for t, char in enumerate(input_text):
          input_seq[0, t, input_token_index[char]] = 1.
     # Используем модель для получения предсказания
     decoded_sentence = decode_sequence(input_seq)
     print(f'Bot reply: {decoded_sentence}')

# Интерактивное общение
while True:
     input_text = input("You: ")
     chat(input_text)