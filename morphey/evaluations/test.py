import importlib
import morphey

from morphey.core.train import get_lemmata, train


def init():
    print('loading the dictionary...', '\n')
    lemmata = get_lemmata()
    print('done', '\n')

    return lemmata


def run(lemmata):
    RNN = importlib.reload(morphey.core.models.RNN).RNN
    train = importlib.reload(morphey.core.train).train

    train(lemmata)
