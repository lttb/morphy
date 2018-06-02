import argparse


def put(*args):
    return input(*args)


def get_args():
    parser = argparse.ArgumentParser('morphey')

    parser.add_argument('-t', '--top', help='top predictions', default='1')

    parser.add_argument(
        '-p', '--proba', help='add probabilities', default=False
    )

    return parser.parse_args()


args = get_args()
