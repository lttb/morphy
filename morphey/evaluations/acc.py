import importlib
import morphey
import time

from morphey.core.train import train, get_lemmata


def init():
    print('loading the dictionary...', '\n')
    lemmata = get_lemmata()
    print('done', '\n')

    return lemmata


def run(lemmata):
    train = importlib.reload(morphey.core.train).train

    [rnn, prepr] = train(lemmata)

    total = 0
    errors = []
    start = time.perf_counter()
    for key, w in list(prepr.Forms.items()):
        total += 1

        v = prepr.vectorize(key)

        cl = prepr.y_encoder.classes_[rnn.model.predict_classes(v)][0]

        is_valid = False
        for s in w:
            if (set(s).issuperset(set(cl))):
                is_valid = True
                break

        if (not is_valid):
            errors.append((key, w, cl))

    end = time.perf_counter()

    print('total: ', total)
    print('acc: ', (total - len(errors)) / total * 100)
    print('errors total: ', len(errors))
    print('time (s): ', end - start)

    print(errors[0:10])

    return [
        lambda x: prepr.y_encoder.classes_[rnn.model.predict_classes(
            prepr.vectorize(x)
        )][0],
        prepr, rnn
    ]


if __name__ == '__main__':
    print('loading the dictionary...', '\n')
    lemmata = get_lemmata()
    print('done', '\n')

    train(lemmata)
