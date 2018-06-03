from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

import xml.etree.cElementTree as ET
import zipfile
import pickle as pickle

from morphey.core.models.Preprocessor import Preprocessor
from morphey.core.models.RNN import RNN

import random
import pathlib

import time


def get_lemmata():
    zf = zipfile.ZipFile('morphey/data/dict.opcorpora.xml.zip', 'r')

    return ET.fromstring(zf.read('dict.opcorpora.xml')).find('lemmata')


def train(lemmata):
    grams_blacklist = {
        'lemma': set([
            # names
            'Abbr',
            'Name',
            'Surn',
            'Patr',
            'Geox',
            'Orgn',
            'Trad',

            # errors
            'Erro',
        ]),
        'form': set([
            'ANim',
            'anim',
            'inan',
        ])
    }

    grams_filter = set([
        'Arch',
        'ANim',
        'anim',
        'inan',
        'perf',
        'impf',
        'tran',
        'intr',

        # needs to reconsider
        'Cmp2'
    ])

    def prepare_grams(g):
        return tuple(
            x.get('v') for x in g.findall('g')
            if x.get('v') not in grams_filter
        )

    prepr = Preprocessor()

    print('preparing the data...', '\n')

    for lemma_node in lemmata.findall('lemma'):
        lemma = lemma_node.find('l')
        grams = prepare_grams(lemma)

        skipped = any(x in grams for x in grams_blacklist['lemma'])
        if (skipped):
            continue

        # base = get_base(lemma.get('t'))
        forms = lemma_node.findall('f')

        for f in forms:
            word = f.get('t')

            form_grams = prepare_grams(f)

            skipped = any(x in form_grams for x in grams_blacklist['form'])
            if (skipped):
                continue

            prepr.add(word, grams + form_grams)

    [x, y] = prepr.fit()

    print('done', '\n')

    _dir = f'morphey/models/rnn/{int(time.time())}'

    with open(f'{_dir}/prepr.pkl', 'wb') as f:
        pickle.dump(prepr, f)

    train_x, test_x, train_y, test_y = train_test_split(
        x, to_categorical(y), test_size=0.30, random_state=random.seed(9)
    )

    rnn = RNN(train_x.shape, len(prepr.y_encoder.classes_))

    res = rnn.model.fit(
        train_x,
        train_y,
        validation_data=(test_x, test_y),
        epochs=5,
        batch_size=64
    )

    pathlib.Path(_dir).mkdir(parents=True, exist_ok=True)

    rnn.model.save(f'{_dir}/base.h5')
    with open(f'{_dir}/meta.pkl', 'wb') as f:
        pickle.dump(res.history, f)

    return [rnn, prepr]


if __name__ == '__main__':
    print('loading the dictionary...', '\n')
    lemmata = get_lemmata()
    print('done', '\n')

    train(lemmata)
