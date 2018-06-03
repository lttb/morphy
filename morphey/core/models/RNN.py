from keras.models import Sequential
from keras.layers import (
    Dense, Dropout, Activation, LSTM, Embedding, Bidirectional, Conv1D,
    MaxPooling1D, BatchNormalization
)


class RNN:
    def __init__(
        self,
        input_shape,
        classes,
        lstm_n=128,
        dropout=0.2,
        kernel_size=3,
        filters=64,
        pool_size=2,
        validation_data=None
    ):
        model = Sequential()

        model.add(Embedding(2000, input_shape[0], input_length=input_shape[1]))
        model.add(Dropout(0.4))
        model.add(
            Conv1D(
                filters=filters,
                kernel_size=kernel_size,
                padding='valid',
                activation='tanh',
                strides=1
            )
        )
        model.add(MaxPooling1D(pool_size))
        model.add(LSTM(classes, return_sequences=False))
        # model.add(Bidirectional(LSTM(classes, return_sequences=True)))
        # model.add(Bidirectional(LSTM(classes)))
        model.add(Dropout(0.2))
        model.add(Dense(classes))
        model.add(BatchNormalization())
        model.add(Activation('softmax'))

        model.compile(
            loss='categorical_crossentropy',
            optimizer='RMSprop',
            metrics=['accuracy'],
        )

        self.model = model
