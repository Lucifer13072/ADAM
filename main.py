from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import numpy as np
import string
import nltk
import configparser
from datetime import date
from keras.preprocessing.sequence import pad_sequences
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

config = configparser.ConfigParser()
config.read("settings.ini")

dt_now = date.today()
np.random.seed(int(config['ADAM']['seed']))

# Загрузка обученной модели
model = tf.keras.models.load_model(f'Out/Out_model_{dt_now}.h5')
metadata = np.load(f'Out/metadata_{dt_now}.npy', allow_pickle=True).item()
model.summary()

# Загрузка метаданных из модели
tokenizer = metadata['tokenizer']
max_length = metadata['max_seq_length']

def preprocess(data):
    # Tokenize data
    tokens = nltk.word_tokenize(data)
    # Lowercase all words
    tokens = [word.lower() for word in tokens]
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('russian'))
    tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation] 
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

def predict_answer(model, tokenizer, question):
    # Preprocess question
    question = preprocess(question)
    # Convert question to sequence
    sequence = tokenizer.texts_to_sequences([question])
    # Pad sequence
    padded_sequence = pad_sequences(sequence, maxlen=max_length)
    # Predict answer
    pred = model.predict(padded_sequence)[0]
    # Get index of highest probability
    idx = np.argmax(pred)
    # Get answer
    answer = tokenizer.index_word[idx]
    return answer

while True:
    question = input('Вопрос: ')
    answer = predict_answer(model, tokenizer, question)
    print('Ответ:', answer)

# question = input('Вопрос: ')
# question_tokens = tokenizer.texts_to_sequences([question])
# question_tokens = pad_sequences(question_tokens, maxlen=max_length)
# answer_tokens = model.predict(question_tokens) # Получение ответа от модели
# answer = tokenizer.sequences_to_texts(answer_tokens)[0] # Преобразование ответа в текст
# print("Вопрос:", question)
# print("Ответ:", answer)