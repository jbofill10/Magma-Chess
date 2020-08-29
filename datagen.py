import keras
import numpy as np
from db import PSQL


class DataGenerator(keras.utils.Sequence):

    def __init__(self, batch_size=32):
        self.db = PSQL()
        self.n = self.db.get_row_count()
        self.idx = np.arange(self.n)
        self.batch_size = batch_size

    def __len__(self):
        return int(np.floor(self.n / self.batch_size))

    # Generate a batch of (X, y)

    def __getitem__(self, index):
        idxs = self.idx[index * self.batch_size:(index + 1) * self.batch_size]

        return self.db.read_records_at(idxs)
