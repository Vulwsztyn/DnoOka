import numpy as np
import warnings
import tensorflow as tf
from tensorflow import keras
from skimage import exposure
import matplotlib.pyplot as plt
import os

warnings.filterwarnings("ignore")
from skimage.io import imread, imsave

if __name__ == '__main__':
    data=np.load('segments/01_dr/0.npz')['arr_0']
    labels = np.load('labels/01_dr/0.npz')['arr_0']
    for i in range(1,23):
        tempS = np.load('segments/01_dr/'+str(i)+'.npz')['arr_0']
        tempL = np.load('labels/01_dr/'+str(i)+'.npz')['arr_0']
        np.concatenate((data,tempS))
        np.concatenate((labels, tempL))

    names=('pixel value','average','mean','average without pixelvalue','labels average')
    for i in range(5):
        for j in range(i+1,5):
                x = [(x[i]) for x in data]
                if j==4:
                    y = [(x[j] / 255) for x in data]
                    # zapomniałem podzielić w oryginale, dalej już będzie podzielone
                else:
                    y = [(x[j]) for x in data]
                plt.scatter(x, y, c=labels,s=0.7)
                plt.xlabel(names[i])
                plt.ylabel(names[j])
                plt.show()