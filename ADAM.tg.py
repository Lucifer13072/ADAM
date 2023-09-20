import tensorflow
from tensorflow import keras
from tensorflow.keras import layers
from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import matplotlib.pyplot as plt
import numpy as np

model = keras.Sequential()


model.add(layers.Embedding(input_dim=1000, output_dim=64))
model.add(layers.LSTM(128))
