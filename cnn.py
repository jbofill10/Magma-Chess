import os, pickle

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from datagen import DataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten


def train():

    model = Sequential([
        Conv2D(filters=8, kernel_size=3, activation='relu', input_shape=(8, 8, 2)),
        # Conv2D(filters=16, kernel_size=3, activation='relu'),
        # Conv2D(filters=32, kernel_size=3, activation='relu'),
        # Conv2D(filters=64, kernel_size=2, activation='relu'),
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
    DataGenerator(batch_size=25).__getitem__(0)
    history = model.fit(DataGenerator(batch_size=120), verbose=1, epochs=100, callbacks=callback)

    if not os.path.isfile('Data/model/model_results'):
        model_hist = history.history

        with open('Data/model_results', 'wb') as file:
            pickle.dump(model_hist, file)
            model.save_weights('Data/model/model_weights')


if __name__ == '__main__':
    train()
