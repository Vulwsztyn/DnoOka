import random

import numpy as np
import warnings
import tensorflow as tf
from tensorflow import keras
from keras import backend as K
warnings.filterwarnings("ignore")
import os
from skimage.io import imread, imsave



def makeTXT(img,mask,result,q,kck):
    # print(mask[0][0])
    # print(mask[1000][1000])
    # print(result[0][0])
    # print(result[1180][760])
    coordsVein=[]
    coordsBlank=[]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if mask[i][j]>0:
                if result[i][j]>0:
                    coordsVein.append([i,j,img[i][j][0],img[i][j][1],img[i][j][2],1,kck[i][j]])
                else:
                    coordsBlank.append([i,j,img[i][j][0],img[i][j][1],img[i][j][2],0,kck[i][j]])
    # sampleBlank=random.sample(coordsBlank,len(coordsVein))
    # folder='txt'
    # if not os.path.exists(folder):
    #     os.makedirs(folder)
    file = open('txt/'+q+'.txt', 'w')
    for i in coordsVein:
        for j in i:
            file.write(str(j)+" ")
        file.write('\n')
    for i in coordsBlank:
        for j in i:
            file.write(str(j) + " ")
        file.write('\n')
    file.close()
    print(q)


if __name__ == '__main__':
    for i in range(1, 16):
        for j in ['h','dr', 'g']:
            myZero = '0'
            if i >= 10:
                myZero = ""
            q=myZero + str(i) + '_' + j
            mask = imread('masks/' + q + '_mask.tif', as_grey=True)
            image = imread('images/'+q+'.jpg')
            result = imread('results/'+q+'.tif')
            kck = 0 #TODO sciezka do Twojego - zakładam, że ma same 0 i 1 i że dla nieistniejacych tez jest decyzja
            makeTXT(image,mask,result,q,kck)
