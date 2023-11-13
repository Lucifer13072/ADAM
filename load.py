from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import numpy as np
import string
import nltk
from nltk import stem
from nltk import corpus
import configparser
from datetime import date
from keras.preprocessing.sequence import pad_sequences
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


# Загрузка обученной модели
model = tf.keras.models.load_model(f'Out/model.h5')
metadata = np.load(f'Out/metadata.npy', allow_pickle=True).item()
model.summary()

# Загрузка метаданных из модели
tokenizer = metadata['tokenizer']
max_length = metadata['max_seq_length']

def preprocess(data):
    tokens = nltk.word_tokenize(data)
    tokens = [word.lower() for word in tokens]
    stop_words = set(stopwords.words('russian'))
    tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation] 
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

def predict_answer(model, tokenizer, question):
    question = preprocess(question)
    sequence = tokenizer.texts_to_sequences([question])
    padded_sequence = pad_sequences(sequence, maxlen=max_length)

    pred = model.predict(padded_sequence)[0]
    idx = np.argmax(pred)
    answer = tokenizer.index_word[idx]
    return answer

while True:
    question = input("Вопрос: ")
    answer = predict_answer(model, tokenizer, question)
    print('Ответ:', answer)