import os, pickle

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


import tensorflow as tf
import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()  #disable for tensorFlow V2
physical_devices = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)
from datagen import DataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten


def train():

    model = Sequential([
        Conv2D(filters=256, kernel_size=3, activation='relu', input_shape=(2, 8, 8), data_format='channels_first'),
        Conv2D(filters=256, kernel_size=3, activation='relu', input_shape=(2, 8, 8), data_format='channels_first'),
        Flatten(),
        Dense(3, activation='softmax')

    ])

    callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=6)

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    model.summary()

    history = model.fit(DataGenerator(batch_size=9021), verbose=1, epochs=20, callbacks=[callback])

    if not os.path.isfile('Data/model/model_results'):
        model_hist = history.history

        with open('Data/model_results', 'wb') as file:
            pickle.dump(model_hist, file)
            model.save_weights('Data/model/model_weights')


if __name__ == '__main__':
    train()
