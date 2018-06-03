# morphy
Morphological Analysis for Russian based on RNNs

## Usage

Run the environment shell for the package:

```
pipenv shell
```

And use `Predictor` to predict grammemes. Keep in mind that it may need some time to load the model to the memory.

```
python

>>> from morphey.core.predict import Predictor
Using TensorFlow backend.

>>> model = Predictor()

>>> model.predict('бутявка')
('NOUN', 'femn', 'sing', 'nomn')

>>> model.predict('бутявкой')
('NOUN', 'femn', 'sing', 'ablt')

>>> model.predict('бутявками')
('NOUN', 'femn', 'plur', 'ablt')
```

> Just to note, on the GitHub stored a really lightweight model, trained on about 50000 lexemes in order not to have too big size. So if you want to get the most accurate results, you can train the model by your side.
