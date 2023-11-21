from keras.models import load_model
import numpy as np
import ADAM
# Загрузка модели
model = load_model('model/Eva1.0.h5')

# Функция для генерации ответа
def generate_response(input_text):
    # Преобразование входного текста в вектор
    encoder_input = np.zeros((1, ADAM.max_encoder_seq_length, ADAM.num_encoder_tokens))
    for t, char in enumerate(input_text):
        if char in ADAM.input_token_index:
            encoder_input[0, t, ADAM.input_token_index[char]] = 1.0
    
    # Генерация ответа с помощью модели
    decoder_input = np.zeros((1, ADAM.max_decoder_seq_length, ADAM.num_decoder_tokens))
    decoder_input[0, 0, ADAM.target_token_index['\t']] = 1.0
    output_text = ''
    for t in range(ADAM.max_decoder_seq_length):
        outputs = model.predict([encoder_input, decoder_input])
        output_token_index = np.argmax(outputs[0, t, :])
        output_char = ADAM.target_characters[output_token_index]
        output_text += output_char
        if output_char == '\n':
            break
        decoder_input[0, t+1, output_token_index] = 1.0
    
    return output_text

# Пример использования
while True:
    question = input("Пользователь: ")
    response = generate_response(question)
    print("ЕВА:", response)
