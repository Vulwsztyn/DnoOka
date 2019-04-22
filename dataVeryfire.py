import numpy as np
import warnings
import tensorflow as tf
from tensorflow import keras
from skimage import exposure
import matplotlib.pyplot as plt
import os
from numpy import genfromtxt
import pandas as pd

warnings.filterwarnings("ignore")
from skimage.io import imread, imsave

if __name__ == '__main__':
    data = genfromtxt('params/01_dr.csv', delimiter=';',names=True)

    names=data.dtype.names
    for i in names[:-1]:
        for j in names[:-1]:
                x = data[i]
                y = data[j]
                plt.scatter(x, y, c=data['dec'],s=0.7)
                plt.xlabel(i)
                plt.ylabel(j)
                plt.show()