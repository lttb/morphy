from os import listdir
from os.path import join

import pickle

from keras.models import load_model

models_dir = 'morphey/models/rnn'

models = sorted(listdir(models_dir))


class Predictor:
    def __init__(self, name=models[-1]):
        self.model = load_model(join(models_dir, name, 'base.h5'))

        with open(join(models_dir, name, 'prepr.pkl'), 'rb') as f:
            self.prepr = pickle.load(f)

    def predict(self, word):
        return self.prepr.y_encoder.classes_[self.model.predict_classes(
            self.prepr.vectorize(word)
        )][0]
