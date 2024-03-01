import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
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
def get_model_response(input_text, loaded_model, tokenizer, max_seq_len):
    input_seq = tokenizer.texts_to_sequences([input_text])
    input_padded = pad_sequences(input_seq, maxlen=max_seq_len, padding='post', truncating='post')
    predictions = loaded_model.predict(input_padded)
    predicted_index = tf.argmax(predictions, axis=-1).numpy()[0][0]  # Extract the first element
    predicted_word = tokenizer.index_word.get(predicted_index, '<OOV>')
    return predicted_word

# Пример использования как чат-бота

def answer(user_input):
    response = get_model_response(user_input, loaded_model, tokenizer, max_seq_len)
    return response