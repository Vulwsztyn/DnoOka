import numpy as np
import warnings
import tensorflow as tf
from tensorflow import keras
from skimage import exposure
import matplotlib.pyplot as plt
import os
from numpy import genfromtxt

warnings.filterwarnings("ignore")
from skimage.io import imread, imsave

if __name__ == '__main__':
    # data=[]
    # for i in range(1, 5):
    #     for j in ['dr', 'h', 'g']:
    #         myZero = '0'
    #         if i >= 10:
    #             myZero = ""
    #         [data.append(x) for x in genfromtxt('params/'+myZero+str(i)+'_'+str(j)+'.csv', delimiter=';',names=True)]
    # data=np.array(data)
    data=genfromtxt('params/01_h.csv', delimiter=';',names=True)
    names=data.dtype.names
    print(names)
    for i in names[:-1]:
        for j in names[:-1]:
            if j!=i:
                x = data[i]
                y = data[j]
                plt.scatter(x, y, c=data['DECYZJA'],s=0.0001)
                plt.xlabel(i)
                plt.ylabel(j)
                plt.show()