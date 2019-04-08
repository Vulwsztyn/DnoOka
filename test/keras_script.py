import numpy as np

import keras
from keras.models import Sequential
from keras.layers import Dense, Activation

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, labels, batch_size=32, dim=(32,32,32), n_channels=1,
                 n_classes=10, shuffle=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()
        self.length

    def __len__(self):
        'Denotes the number of batches per epoch'
        return self.length

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch


        # Generate data
        X, y = self.__data_generation(str(index))

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, ID):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, self.dim, self.n_channels))
        y = np.empty((self.batch_size), dtype=int)

        X = np.load('data/' + ID + '.npz')
        self.length=len(X)

        y = np.load('labels/' + ID + '.npz')

        return X, keras.utils.to_categorical(y, num_classes=self.n_classes)

# Parameters
params = {'dim': (32,32,32),
          'batch_size': 64,
          'n_classes': 6,
          'n_channels': 1,
          'shuffle': True}

# Datasets
train=[]
for i in range(20):
    train.append(i)
test=[]
for i in range(21,24):
    test.append(i)
labels = []
for i in range(24):
    labels.append(i)

array=(np.load('data/0.npz'))
print(np.array(array['arr_0']).shape)



# # Generators
# training_generator = DataGenerator(train, labels, **params)
# validation_generator = DataGenerator(test, labels, **params)
#
# # Design model
# model = Sequential()
# model.add(Dense(81, activation='sigmoid', input_dim=81))
# model.add(Dense(2, activation='sigmoid'))
# model.compile()
#
# # Train model on dataset
# model.fit_generator(generator=training_generator,
#                     validation_data=validation_generator,
#                     use_multiprocessing=True,
#                     workers=6)
