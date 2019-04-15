import numpy as np
import warnings
import tensorflow as tf
from tensorflow import keras
from keras import backend as K
from keras.utils import to_categorical
from keras import optimizers
import pandas as pd


warnings.filterwarnings("ignore")
from skimage.io import imread, imsave
import matplotlib.pyplot as plt


def plot_confusion_matrix(df_confusion, title='Confusion matrix', cmap=plt.cm.gray_r):
    plt.matshow(df_confusion, cmap=cmap)  # imshow
    # plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(df_confusion.columns))
    plt.xticks(tick_marks, df_confusion.columns, rotation=45)
    plt.yticks(tick_marks, df_confusion.index)
    # plt.tight_layout()
    plt.ylabel(df_confusion.index.name)
    plt.xlabel(df_confusion.columns.name)
    plt.show()

def precision(y_true, y_pred):
    """Precision metric.
    Only computes a batch-wise average of precision. Computes the precision, a
    metric for multi-label classification of how many selected items are
    relevant.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def recall(y_true, y_pred):
    """Recall metric.
    Only computes a batch-wise average of recall. Computes the recall, a metric
    for multi-label classification of how many relevant items are selected.
    """
    true_positives = K.sum(y_true * y_pred)
    possible_positives = K.sum(y_true)
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def f1_score(y_true, y_pred):
    """
    f1 score

    :param y_true:
    :param y_pred:
    :return:
    """
    tp_3d = K.concatenate(
        [
            K.cast(y_true, 'bool'),
            K.cast(K.round(y_pred), 'bool'),
            K.cast(K.ones_like(y_pred), 'bool')
        ], axis=1
    )

    fp_3d = K.concatenate(
        [
            K.cast(K.abs(y_true - K.ones_like(y_true)), 'bool'),
            K.cast(K.round(y_pred), 'bool'),
            K.cast(K.ones_like(y_pred), 'bool')
        ], axis=1
    )

    fn_3d = K.concatenate(
        [
            K.cast(y_true, 'bool'),
            K.cast(K.abs(K.round(y_pred) - K.ones_like(y_pred)), 'bool'),
            K.cast(K.ones_like(y_pred), 'bool')
        ], axis=1
    )

    tp = K.sum(K.cast(K.all(tp_3d, axis=1), 'int32'))
    fp = K.sum(K.cast(K.all(fp_3d, axis=1), 'int32'))
    fn = K.sum(K.cast(K.all(fn_3d, axis=1), 'int32'))

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return 2 * ((precision * recall) / (precision + recall))

def confusion(y_true, y_pred):
    y_pred_pos = K.round(K.clip(y_pred, 0, 1))
    y_pred_neg = 1 - y_pred_pos
    y_pos = K.round(K.clip(y_true, 0, 1))
    y_neg = 1 - y_pos
    tp = K.sum(y_pos * y_pred_pos) / K.sum(y_pos)
    tn = K.sum(y_neg * y_pred_neg) / K.sum(y_neg)
    return tp


class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, batch_size=32,n_classes=10):
        'Initialization'
        self.batch_size = batch_size
        self.list_IDs = list_IDs
        self.n_classes = n_classes

    def __len__(self):
        'Denotes the number of batches per epoch'
        return len(self.list_IDs)

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        X, y = self.__data_generation(self.list_IDs[index])
        return X, y


    def __data_generation(self, ID):
        # Generate data
        X = np.load('segments/01_dr/' + ID + '.npz')['arr_0']
        y = np.load('labels/01_dr/' + ID + '.npz')['arr_0'] / 255
        y=to_categorical(y)
        return X, y


if __name__ == '__main__':

    train_images=[]
    test_image=['1']
    for i in range(2, 24):
        train_images.append(str(i))

    params = {'batch_size': 1,
              'n_classes': 2}



    training_generator = DataGenerator(train_images, **params)
    validation_generator = DataGenerator(test_image, **params)

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(9, 9)),
        keras.layers.Dense(81, activation=tf.nn.sigmoid),
        keras.layers.Dense(81, activation=tf.nn.sigmoid),
        keras.layers.Dense(81, activation=tf.nn.sigmoid),
        keras.layers.Dense(2, activation=tf.nn.sigmoid)
    ])
    print("compile model")
    model.compile(optimizer='sgd',loss='categorical_crossentropy',
                  metrics=[recall])
    print("fit model")
    model.fit_generator(generator=training_generator,
                        validation_data=validation_generator, epochs=1)
    print("test model")
    test_images = np.load('segments/01_h/1.npz')['arr_0']
    test_labels=np.load('labels/01_h/1.npz')['arr_0'] / 255

    predicted = model.predict(test_images)
    # show the inputs and predicted outputs

    predicted_class=[]
    for i in range(len(test_labels)):
        if predicted[i][0]<predicted[i][1]*2:
            predicted_class.append(1)
        else:
            predicted_class.append(0)

    y_actu = pd.Series(test_labels, name='Actual')
    y_pred = pd.Series(predicted_class, name='Predicted')
    df_confusion = pd.crosstab(y_actu, y_pred)


    plot_confusion_matrix(df_confusion)

