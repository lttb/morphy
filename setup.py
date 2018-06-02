from setuptools import find_packages, setup

setup(
    name='morphey',
    packages=find_packages(),
    version='0.0.1',
    description='Morphological Analysis for Russian based on RNNs',
    author='Kenzhaev Artur',
    author_email='kenzhaev.artur@gmail.com',
    url='https://github.com/lttb/morphy',
    install_requires=[
        'keras>=2.1.6',
        'numpy>=1.14.0',
        'pymorphy2>=0.8',
        'russian-tagsets==0.6',
        'scikit-learn>=0.19.1',
        'scipy>=1.0.0',
        'tensorflow>=1.8.0',
    ],
    setup_requires=['flake8', 'flake8-quotes', 'pyre-check', 'yapf']
)
