import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
import numpy as np
import json
import pickle

model_path = 'model/model.h5'
loaded_model = load_model(model_path)

with open('model/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('model/max_seq_len.pickle', 'rb') as handle:
    max_seq_len = pickle.load(handle)

# Функция предобработки входного текста
def preprocess_input_text(text, tokenizer, max_seq_len):
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_seq_len, padding='post', truncating='post')
    return padded_sequence

# Функция для получения ответа от модели
def get_model_response(input_sequence, loaded_model):
    predictions = loaded_model.predict(input_sequence)
    predicted_index = tf.argmax(predictions, axis=-1).numpy()[0][0] 
    predicted_word = tokenizer.index_word.get(predicted_index, '<OOV>')
    return predicted_word

# Пример использования как чат-бота
def answer(user_input):
    input_sequence = preprocess_input_text(user_input, tokenizer, max_seq_len)
    dummy_decoder_input = np.zeros_like(input_sequence)  # Создайте фиктивный вход для декодера
    response = get_model_response([input_sequence, dummy_decoder_input], loaded_model)
    return response
