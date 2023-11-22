from keras.models import Model, load_model
from keras.layers import Input
import numpy as np
import ADAM

# Загрузка предварительно обученной модели
model = load_model('EVA_model.h5')
encoder_inputs = model.input[0]  # input_1
encoder_outputs, state_h_enc, state_c_enc = model.layers[2].output  # lstm_1
encoder_states = [state_h_enc, state_c_enc]
encoder_model = Model(encoder_inputs, encoder_states)

decoder_inputs = model.input[1]  # input_2
decoder_state_input_h = Input(shape=(256,), name='input_3')
decoder_state_input_c = Input(shape=(256,), name='input_4')
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_lstm = model.layers[3]
decoder_outputs, state_h_dec, state_c_dec = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
decoder_states = [state_h_dec, state_c_dec]
decoder_dense = model.layers[4]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model([decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)

# Функция для генерации ответа на вопрос
def decode_sequence(input_seq):
    # Кодирование ввода как вектора состояния
    states_value = encoder_model.predict(input_seq)

    # Генерация пустого целевого последовательности одного элемента.
    target_seq = np.zeros((1, 1, ADAM.num_decoder_tokens))
    # Заполнение первого символа целевой последовательности значением начала последовательности.
    target_seq[0, 0, ADAM.target_token_index['\t']] = 1.

    # Итеративное декодирование в одном байте за раз
    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)
        # Декодирование токена
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = ADAM.reverse_target_char_index[sampled_token_index]
        decoded_sentence += sampled_char

        # Выход: либо найден символ конца строки, либо достигнута максимальная длина.
        if (sampled_char == '\n' or len(decoded_sentence) > ADAM.max_decoder_seq_length):
            stop_condition = True

        # Обновление целевой последовательности (длиной 1).
        target_seq = np.zeros((1, 1, ADAM.num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.

        # Обновление состояний.
        states_value = [h, c]

    return decoded_sentence

# Использование модели для генерации ответа на входной вопрос
def answer_question(question):
    encoder_input_data = np.zeros((1, ADAM.max_encoder_seq_length, ADAM.num_encoder_tokens), dtype='float32')
    for t, char in enumerate(question):
        encoder_input_data[0, t, ADAM.input_token_index[char]] = 1.

    return decode_sequence(encoder_input_data)

# Тестирование бота с некоторыми вопросами
while True:
    question = input('Введите вопрос: ')
    print(answer_question(question))