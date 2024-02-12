from keras.models import load_model
from keras.layers import Input, LSTM, Dense
from keras.models import Model
import numpy as np
import json

# Загрузка необходимых данных
with open('model/required_data.json', 'r', encoding='utf-8') as f:
    required_data = json.load(f)

num_decoder_tokens = required_data['num_decoder_tokens']
max_decoder_seq_length = required_data['max_decoder_seq_length']
latent_dim = required_data['latent_dim']
input_token_index = required_data['input_token_index']
target_token_index = required_data['target_token_index']
reverse_target_char_index = required_data['reverse_target_char_index']

# Загрузка модели
model = load_model('model/EVA_model.h5')

def answer(text):
    answer_txt = text + " 123"
    return answer_txt