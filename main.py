import tensorflow as tf
import numpy as np
from datetime import date
from keras.preprocessing.sequence import pad_sequences

dt_now = date.today()

# Загрузка обученной модели
model = tf.keras.models.load_model(f'Out/Out_model_{dt_now}.h5')

# Загрузка метаданных модели
metadata = np.load(f'Out/metadata_{dt_now}.npy', allow_pickle=True).item()
tokenizer = metadata['tokenizer']
max_length = metadata['max_seq_length']

question = input('Вопрос: ')

question_tokens = tokenizer.texts_to_sequences([question])
question_tokens = pad_sequences(question_tokens, maxlen=max_length)

# Получение ответа от модели
answer_tokens = model.predict(question_tokens)

# Преобразование ответа в текст
answer = tokenizer.sequences_to_texts(answer_tokens)[0]

print("Вопрос:", question)
print("Ответ:", answer)