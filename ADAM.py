from __future__ import absolute_import, division, print_function, unicode_literals
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import json
import numpy as np
from keras.models import Model
from keras.layers import Input, LSTM, Dense

# Чтение файла и загрузка данных
with open('dataset/dataset.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read(), strict=False)

# Подготовка входных и выходных данных
input_texts = []
target_texts = []
input_characters = set()
target_characters = set()

for line in data:
    input_text = line['Вопрос']
    target_text = line['Ответ']

    input_texts.append(input_text)
    target_texts.append(target_text)

    for char in input_text:
        if char not in input_characters:
            print(f"Adding {repr(char)} to input_characters")
            input_characters.add(char)
        
            

    for char in target_text:
        if char not in target_characters:
            print(f"Adding {repr(char)} to target_characters")
            target_characters.add(char)

input_characters = sorted(list(input_characters))
target_characters = sorted(list(target_characters))
num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = max([len(txt) for txt in input_texts])
max_decoder_seq_length = max([len(txt) for txt in target_texts])

# Определение словарей для перевода символов в индексы и обратно
input_token_index = dict([(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict([(char, i) for i, char in enumerate(target_characters)])
reverse_input_char_index = dict((i, char) for char, i in input_token_index.items())
reverse_target_char_index = dict((i, char) for char, i in target_token_index.items())

# Подготовка входных и выходных данных в формате one-hot
encoder_input_data = np.zeros((len(input_texts), max_encoder_seq_length, num_encoder_tokens), dtype='float32')
decoder_input_data = np.zeros((len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype='float32')
decoder_target_data = np.zeros((len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype='float32')

for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
    for t, char in enumerate(input_text):
        encoder_input_data[i, t, input_token_index[char]] = 1.0
    for t, char in enumerate(target_text):
        decoder_input_data[i, t, target_token_index[char]] = 1.0
        if t > 0:
            decoder_target_data[i, t - 1, target_token_index[char]] = 1.0

# Определение размерности и конфигурации модели
latent_dim = 256

encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder = LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]

decoder_inputs = Input(shape=(None, num_decoder_tokens))
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = Dense(num_decoder_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Создание модели
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Компиляция модели
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

# Обучение модели
epochs = 10
batch_size = 64
model.fit(
    [encoder_input_data, decoder_input_data],
    decoder_target_data,
    batch_size=batch_size,
    epochs=epochs,
    validation_split=0.2
)

# Сохранение модели на диск
model.save('model/EVA_model.h5')

# Сохранение модели на диск
model.save('model/EVA_model.h5')

required_data = {
    'num_decoder_tokens': num_decoder_tokens,
    'max_decoder_seq_length': max_decoder_seq_length,
    'latent_dim': latent_dim,
    'input_token_index': input_token_index,
    'target_token_index': target_token_index,
    'reverse_target_char_index': reverse_target_char_index
}

with open('model/required_data.json', 'w', encoding='utf-8') as f:
    json.dump(required_data, f, ensure_ascii=False, indent=4)

print("Input tokens:")
print(input_token_index)

print("Target tokens:")
print(target_token_index)
