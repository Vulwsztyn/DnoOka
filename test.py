import numpy as np

import keras
from keras.models import Sequential
from keras.layers import Dense, Activation

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self,list_IDs, batch_size=32, dim=(32,32,32), n_channels=1,
                 n_classes=2, shuffle=True):
        'Initialization'
        self.dim = dim
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()
        self.length=0

    def __len__(self):
        'Denotes the number of batches per epoch'
        return len(self.list_IDs)

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch

        # Generate data
        X, y = self.__data_generation(self.list_IDs[index])

        return X, y


    def __data_generation(self, ID):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization

        X = np.load('segments/01_h' + ID + '.npz')['arr_0']
        self.length=len(X)

        y = np.load('labels/01_h' + ID + '.npz')['arr_0']
        y=y/255

        return X, keras.utils.to_categorical(y, num_classes=self.n_classes)

if __name__ == '__main__':
    # Parameters
    params = {'dim': (9,9),
              'batch_size': 64,
              'n_classes': 2,
              'n_channels': 1,
              'shuffle': True}

    # Datasets
    train=[]
    for i in range(1,21):
        train.append(str(i))
    test=[]
    for i in range(21,25):
        test.append(str(i))

    print(train,test)



    # Generators
    training_generator = DataGenerator(train,**params)
    validation_generator = DataGenerator(test,**params)

    # Design model
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(9, 9)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(1, activation='softmax')
    ])

    model.compile(generator=training_generator,
                  validation_data=validation_generator,
                  optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    # Train model on dataset
    model.fit_generator(generator=training_generator,
                        validation_data=validation_generator,
                        use_multiprocessing=True,
                        workers=1)