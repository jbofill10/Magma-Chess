import os, pickle

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()  #disable for tensorFlow V2

from datagen import DataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten, BatchNormalization


class CovNet:
    
    def __init__(self):
        model = Sequential([
            Conv2D(filters=256, kernel_size=3, activation='relu', input_shape=(7, 8, 8), data_format='channels_first'),
            # BatchNormalization(),
            Conv2D(filters=256, kernel_size=3, activation='relu'),
            Flatten(),
            Dense(3, activation='softmax')

        ])

        self.callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=6)
        self.checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath='model/checkpoint/weights.{epoch:02d}-{loss:.2f}.hdf5',
                                                             monitor='loss',
                                                             save_best_only=True,
                                                             save_freq='epoch')

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        self.model = model

        if os.path.isfile('Data/model/model_weights.h5'):

            model.load_weights('Data/model/model_weights.h5')
        else:

            model.summary()

    def train(self):
    
        history = self.model.fit(DataGenerator(batch_size=25), verbose=1, epochs=7, callbacks=[self.callback])

        model_hist = history.history

        with open('Data/model_results', 'wb') as file:
            pickle.dump(model_hist, file)
            self.model.save_weights('Data/model/model_weights.h5')

    def predict(self, x):

        y = self.model.predict(x)

        return y[0].tolist()

