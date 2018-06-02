from typing import List

from sklearn.preprocessing import LabelEncoder, Imputer
from keras.preprocessing.sequence import pad_sequences

from ..utils.sylls import custom

Hashes = dict()

Sylls = dict()
Sylls_idx = dict()

MISSED = -1

split_sylls = custom.split


class Preprocessor:
    def __init__(self):
        self.x = []
        self.y = []
        self.Forms = dict()

        self.y_encoder = LabelEncoder()
        self.x_encoder = Imputer(missing_values=MISSED)

        self.x_maxlen = 5

    def add(self, form, grams):
        x = get_vector(form)
        y = grams

        if (form not in self.Forms):
            self.Forms[form] = set()

        self.Forms[form].add(y)

        self.x.append(x)
        self.y.append(y)

    def pad_x(self, x):
        return pad_sequences(
            x,
            truncating='post',
            padding='post',
            maxlen=self.x_maxlen,
            value=MISSED
        )

    def vectorize(self, word):
        vector = get_vector(word)
        return self.transform_x([vector])

    def transform_x(self, x):
        return self.x_encoder.transform(self.pad_x(x))

    def fit(self, x=None, y=None):
        if (x and y):
            for i, form in enumerate(x):
                self.add(form, y[i])

        y_fitted = self.y_encoder.fit_transform(self.y)
        x_fitted = self.x_encoder.fit_transform(self.pad_x(self.x))

        return [x_fitted, y_fitted]


def normalize(word: str) -> str:
    return word.replace('ё', 'е')


def get_hash(s: str) -> int:
    if (s not in Sylls):
        i = len(Sylls)
        Sylls[s] = i
        Sylls_idx[i] = s
    return Sylls[s]


def get_vector(word: str) -> List[int]:
    word = normalize(word)

    sylls = split_sylls(word)
    arr = reversed(sylls)

    vector = []
    for syll in arr:
        vector.append(get_hash(syll))

    return vector


def get_base(lemma: str, forms) -> str:
    base = normalize(lemma)

    # calc base
    for f in forms:
        word = normalize(f.get('t'))

        i = 0
        while (base not in word):
            i = i + 1
            base = base[:-i]

    return base
