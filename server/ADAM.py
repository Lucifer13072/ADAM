import matplotlib.pyplot as plt
from keras.layers import Input, Embedding, Dense, Dropout, LayerNormalization, MultiHeadAttention, concatenate
from keras.models import Model
from keras.layers import Add
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import json
import pickle
import os


# Загрузка и предобработка данных
def load_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)
    questions = [item['Вопрос'] for item in dataset]
    answers = [item['Ответ'] for item in dataset]
    return questions, answers

def preprocess_data(questions, answers):
    tokenizer = Tokenizer(oov_token='<OOV>')
    tokenizer.fit_on_texts(questions + answers)

    questions_seq = tokenizer.texts_to_sequences(questions)
    answers_seq = tokenizer.texts_to_sequences(answers)

    max_seq_len = max(max(len(seq) for seq in questions_seq), max(len(seq) for seq in answers_seq))
    
    questions_padded = pad_sequences(questions_seq, maxlen=max_seq_len, padding='post', truncating='post')
    answers_padded = pad_sequences(answers_seq, maxlen=max_seq_len, padding='post', truncating='post')

    with open('../client/model/tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('../client/model/max_seq_len.pickle', 'wb') as handle:
        pickle.dump(max_seq_len, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return questions_padded, answers_padded, tokenizer, max_seq_len

# Создание модели
def transformer_chatbot_model(input_dim, num_heads, ff_dim, max_seq_len, vocab_size, dropout=0.1):
    # Вход для вопросов
    encoder_inputs = Input(shape=(max_seq_len,))
    # Вход для ответов
    decoder_inputs = Input(shape=(max_seq_len,))

    # Embedding слой для преобразования входных слов в вектора
    embedding_layer = Embedding(input_dim=vocab_size, output_dim=input_dim)

    encoder_embedding = embedding_layer(encoder_inputs)
    decoder_embedding = embedding_layer(decoder_inputs)

    # Multi-Head Attention для вопросов
    encoder_attention = MultiHeadAttention(num_heads=num_heads, key_dim=input_dim)(encoder_embedding, encoder_embedding)
    encoder_attention = Dropout(dropout)(encoder_attention)
    encoder_output = LayerNormalization(epsilon=1e-6)(encoder_embedding + encoder_attention)

    # Multi-Head Attention для ответов
    decoder_attention = MultiHeadAttention(num_heads=num_heads, key_dim=input_dim)(decoder_embedding, decoder_embedding)
    decoder_attention = Dropout(dropout)(decoder_attention)
    decoder_output = LayerNormalization(epsilon=1e-6)(decoder_embedding + decoder_attention)

    # Объединение выходов
    combined_output = Add()([encoder_output, decoder_output])

    # Feed Forward Part
    x = Dense(ff_dim, activation="relu")(combined_output)
    x = Dense(input_dim)(x)
    x = Dropout(dropout)(x)
    output = LayerNormalization(epsilon=1e-6)(combined_output + x)

    # Создание модели
    model = Model(inputs=[encoder_inputs, decoder_inputs], outputs=output)
    return model

# Загрузка данных и предобработка
file_path = 'dataset/dataset.json'  # Укажите путь к вашему датасету
questions, answers = load_dataset(file_path)
questions_padded, answers_padded, tokenizer, max_seq_len = preprocess_data(questions, answers)

# Создание и компиляция модели
vocab_size = len(tokenizer.word_index) + 1  # +1 для учета токена <OOV>
num_attention_heads = 8
feed_forward_dimension = 2048
# Создание и компиляция модели
chatbot_model = transformer_chatbot_model(input_dim=512, num_heads=num_attention_heads, ff_dim=feed_forward_dimension,
                                          max_seq_len=max_seq_len, vocab_size=vocab_size)

chatbot_model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=['accuracy'])

# Обучение модели
history = chatbot_model.fit([questions_padded, answers_padded], answers_padded, epochs=10, batch_size=64, validation_split=0.2)

# Вывод графика потерь
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.savefig("grafics/loss.jpg")

# Вывод графика точности
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig("grafics/accuracy.jpg")

chatbot_model.save("../client/model/model.h5")