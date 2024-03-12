import numpy as np
import tensorflow as tf
from keras import layers, models, optimizers
import os
import numpy as np
import librosa

def extract_features(file_path, mfcc_dim=40):
    audio, _ = librosa.load(file_path, sr=16000)  # Загрузка аудиофайла
    mfccs = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=mfcc_dim)  # Извлечение MFCC коэффициентов
    return mfccs


file_list = os.listdir('dataset/audiodata/')

# Извлечение признаков и меток классов
X = []
y = []
for file_name in file_list:
    file_path = os.path.join('dataset/audiodata/', file_name)
    mfccs = extract_features(file_path)
    X.append(mfccs)
    # Предполагаем, что метки классов включены в имена файлов (например, sound_class_1.wav)
    label = int(file_name.split('_')[2])  # Предполагаем, что метка класса находится в третьей части имени файла
    y.append(label)

# Преобразование в numpy массивы
X = np.array(X)
y = np.array(y)

# Генерация случайных данных для примера
X_train = np.random.rand(100, 10, 40)  # Примерный формат данных: (количество_примеров, длина_последовательности, размер_признаков)
y_train = np.random.randint(0, 256, (100, 10))  # Примерный формат меток: (количество_примеров, длина_последовательности)

# Модель
def build_model(input_shape, output_dim, hidden_dim=256):
    model = models.Sequential([
        layers.Bidirectional(layers.LSTM(hidden_dim, return_sequences=True), input_shape=input_shape),
        layers.Dropout(0.2),
        layers.TimeDistributed(layers.Dense(output_dim)),
        layers.Activation('softmax')
    ])
    return model

input_shape = X.shape[1:]
output_dim = len(np.unique(y))  

model = build_model(input_shape, output_dim)
optimizer = optimizers.Adam(lr=0.001)
model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
model.summary()

# Обучение модели
batch_size = 32
epochs = 10

model.fit(X, y, batch_size=batch_size, epochs=epochs, validation_split=0.1)

model.save("../client/model/tts_Eva_model.h5")