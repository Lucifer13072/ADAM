import numpy as np
import pickle
from keras.models import load_model, Model
from keras.layers import Input


# Загрузка необходимых данных
with open('model/required_data.pkl', 'rb') as f:
    required_data = pickle.load(f)

num_decoder_tokens = required_data['num_decoder_tokens']
max_decoder_seq_length = required_data['max_decoder_seq_length']
latent_dim = required_data['latent_dim']
input_token_index = required_data['input_token_index']
target_token_index = required_data['target_token_index']
reverse_target_char_index = required_data['reverse_target_char_index']

# Загрузка модели на диск
model = load_model('model/EVA_model.h5')

# Определение модели кодировщика
encoder_inputs = model.input[0]
encoder_outputs, state_h_enc, state_c_enc = model.layers[2].output
encoder_states = [state_h_enc, state_c_enc]
encoder_model = Model(encoder_inputs, encoder_states)

# Определение модели декодировщика
decoder_inputs = model.input[1]
decoder_state_input_h = Input(shape=(latent_dim,), name='input_3')
decoder_state_input_c = Input(shape=(latent_dim,), name='input_4')
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_lstm = model.layers[3]
decoder_outputs, state_h_dec, state_c_dec = decoder_lstm(
    decoder_inputs, initial_state=decoder_states_inputs
)
decoder_states = [state_h_dec, state_c_dec]
decoder_dense = model.layers[4]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs,
    [decoder_outputs] + decoder_states
)

def decode_sequence(input_seq):
    # Encode the input as state vectors.
    states_value = encoder_model.predict(input_seq)

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    
    # Populate the first character of target sequence.
    target_seq[0, 0, target_token_index['\t']] = 1.

    # Sampling loop for a batch of sequences
    stop_condition = False
    decoded_sentence = ''
    
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += sampled_char

        # Exit condition: either hit max length
        # or find stop character.
        if sampled_char == '\n' or len(decoded_sentence) > max_decoder_seq_length:
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.

        # Update states
        states_value = [h, c]

    return decoded_sentence

while True:
    input_text = input()
    input_texts = []
    input_characters = set()
    target_characters = set()
    input_texts.append(input_text)

    for char in input_text:
        if char not in input_characters:
            input_characters.add(char)

    max_encoder_seq_length = max([len(txt) for txt in input_texts])
    num_encoder_tokens = len(input_characters)

    # Подготовка входного текста
    input_seq = np.zeros((1, max_encoder_seq_length, num_encoder_tokens), dtype='float32')
    print(input_seq)
    # check that characters in input_text are all in input_token_index
    # for t, char in enumerate(input_text):
    #     if char in input_token_index:
    #         input_seq[0, t, input_token_index[char]] = 1
    #     else:
    #         print(f"Character {char} not recognized by the model.")
    #         break

    # Декодирование входного текста
    decoded_sentence = decode_sequence(input_seq)
    print('Decoded sentence:', decoded_sentence)