import numpy as np
import warnings
import tensorflow as tf
from tensorflow import keras

warnings.filterwarnings("ignore")
from skimage.io import imread, imsave


def podzialNaCzesci(img, res,mask, n=9,ilePerPlik=288193):
    if n % 2 == 0:
        raise ValueError("Wymiar maski ma być nieparzysty")
    margines = n // 2
    czesci = []
    fileCounter = 0
    result = []
    for i in range(margines, img.shape[0] - margines):
        print('i',i)
        # print(i - margines, ' out of ', img.shape[0] - margines - margines)
        for j in range(margines, img.shape[1] - margines):
            if mask[i][j] > 0.0:
                czesc = []
                for a in range(-margines, n - margines, 1):
                    wiersz = []
                    for b in range(-margines, n - margines, 1):
                        wiersz.append(img[i + a][j + b])
                    czesc.append(wiersz)
                if np.average(czesc) > 0.1:
                    result.append(res[i][j])
                    czesci.append(czesc)
        if len(czesci)>=ilePerPlik:
            np.savez_compressed('segments/01_h/' + str(fileCounter), np.array(czesci))
            np.savez_compressed('labels/01_h/' + str(fileCounter), np.array(result))
            czesci = []
            result = []
            fileCounter+=1
    i=-1
    while len(czesci)<ilePerPlik:
        czesci.append(czesci[i])
        result.append(result[i])
        i-=1
    np.savez_compressed('segments/01_h/' + str(fileCounter), np.array(czesci))
    np.savez_compressed('labels/01_h/' + str(fileCounter), np.array(result))


def toGrey(image, whichChannel):
    for i in range(len(image)):
        for j in range(len(image[whichChannel])):
            image[i][j] = image[i][j][whichChannel]
    return image



if __name__ == '__main__':
    # print("reading")
    # image = imread('images/01_h.jpg', as_gray=True)
    # result = imread('results/01_h.tif')
    # mask = imread('masks/01_h_mask.tif', as_grey=True)
    # print("podzieling")
    # podzialNaCzesci(image, result, mask,9)
    isTestSet=isTrainSet=False
    for i in range(0,1):
        if not isTestSet:
            test_images = np.load('segments/01_h/'+str(i)+'.npz')['arr_0']
            test_labels = np.load('labels/01_h/'+str(i)+'.npz')['arr_0'] / 255
            isTestSet=True


    for i in range(1,24):
        print('wczytuje',i+1,'na 24')
        a = np.load('segments/01_h/'+str(i)+'.npz')['arr_0']
        b = np.load('labels/01_h/'+str(i)+'.npz')['arr_0'] / 255
        # Nie umiem inicjalizowac
        if not isTrainSet:
            train_images = a
            train_labels = b
            isTrainSet=True
        else:
            train_images = np.concatenate([train_images, a])
            train_labels = np.concatenate([train_labels, b])

    print(train_images.shape)
    print(train_labels.shape)
    print(test_images.shape)
    print(test_labels.shape)

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(9,9)),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(1, activation=tf.nn.softmax)
    ])
    print("compile model")
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    print("fit model")
    model.fit(train_images, train_labels, epochs=10)
    print("test model")
    test_loss, test_acc = model.evaluate(test_images, test_labels)

    print('Test accuracy:', test_acc)

    # print(type(train_images))
    # model = keras.Sequential([
    #     keras.layers.Flatten(input_shape=(9, 9)),
    #     keras.layers.Dense(128, activation='relu'),
    #     keras.layers.Dense(1, activation='softmax')
    # ])
    #
    # model.compile(optimizer='adam',
    #               loss='binary_crossentropy',
    #               metrics=['accuracy'])
    #
    # model.fit(train_images, train_labels, epochs=1)
