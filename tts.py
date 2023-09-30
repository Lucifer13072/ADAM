


#НЕ РАБОТАЕТ
#В ПРОЦЕССЕ СОЗДАНИЯ



import tensorflow as tf
from tensorflow import keras
from keras.layers import Input, LSTM, Dense
from keras.models import Model

# Задаем параметры модели
input_dim = 100 # Размерность входного вектора (размерность эмбеддинга текста)
hidden_units = 256 # Количество скрытых единиц LSTM
output_dim = 1 # Размерность выходного вектора (одно число - озвученный тембр)

# Определяем архитектуру модели
inputs = Input(shape=(None, input_dim)) # Входной слой - переменная длина последовательности
lstm = LSTM(hidden_units, return_sequences=True)(inputs) # Слой LSTM
outputs = Dense(output_dim, activation='sigmoid')(lstm) # Выходной слой с одним выходом

# Создаем модель
model = Model(inputs=inputs, outputs=outputs)

# Компилируем модель
model.compile(optimizer='adam', loss='mse')

# Обучаем модель
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Используем обученную модель для генерации озвученного текста
predictions = model.predict(X_test)