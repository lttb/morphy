from typing import List

from sklearn.preprocessing import LabelEncoder, Imputer
from keras.preprocessing.sequence import pad_sequences

from ..utils.sylls import custom

Hashes = dict()

MISSED = -1

split_sylls = custom.split


def normalize(word: str) -> str:
    return word.replace('ё', 'е')


class Preprocessor:
    def __init__(
        self, x=[], y=[], Forms=dict(), Sylls=dict(), Sylls_idx=dict()
    ):
        self.x = x
        self.y = y
        self.Forms = Forms
        self.Sylls = Sylls
        self.Sylls_idx = Sylls_idx

        self.y_encoder = LabelEncoder()
        self.x_encoder = Imputer(missing_values=MISSED)

        self.x_maxlen = 5

    def add(self, form, grams):
        x = self.get_vector(form)
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
        vector = self.get_vector(word)
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

    def get_hash(self, s: str) -> int:
        if (s not in self.Sylls):
            i = len(self.Sylls)
            self.Sylls[s] = i
            self.Sylls_idx[i] = s
        return self.Sylls[s]

    def get_vector(self, word: str) -> List[int]:
        word = normalize(word)

        sylls = split_sylls(word)
        arr = reversed(sylls)

        vector = []
        for syll in arr:
            vector.append(self.get_hash(syll))

        return vector

    # def get_base(self, lemma: str, forms) -> str:
    #     base = self.normalize(lemma)
    #
    #     # calc base
    #     for f in forms:
    #         word = self.normalize(f.get('t'))
    #
    #         i = 0
    #         while (base not in word):
    #             i = i + 1
    #             base = base[:-i]
    #
    #     return base
