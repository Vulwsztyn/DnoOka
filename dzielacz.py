import numpy as np
import warnings
import tensorflow as tf
from tensorflow import keras
from skimage import exposure
import os

warnings.filterwarnings("ignore")
from skimage.io import imread, imsave


def podzialNaCzesci(img, res,mask,numer,typ,n=9,ilePerPlik=288193):
    q=numer
    print(q,typ)
    if n % 2 == 0:
        raise ValueError("Wymiar maski ma być nieparzysty")
    margines = n // 2
    czesci = []
    fileCounter = 0
    result = []
    positive=[]
    negative=[]
    for i in range(margines, img.shape[0] - margines):
        # print('i',i)
        print(i - margines, ' out of ', img.shape[0] - margines - margines)
        for j in range(margines, img.shape[1] - margines):
            if mask[i][j] > 0.0:
                czesc = []
                for a in range(-margines, n - margines, 1):
                    wiersz = []
                    for b in range(-margines, n - margines, 1):
                        wiersz.append(img[i + a][j + b])
                    czesc.append(wiersz)
                parameters = []
                parameters.append(img[i][j])
                parameters.append(np.average(czesc))
                parameters.append(np.mean(czesc))
                parameters.append((np.sum(czesc) - img[i][j]) / ((n ** 2) - 1))
                if res[i][j]>0.5:
                    positive.append(parameters)
                else:
                    negative.append(parameters)
            if len(positive)+len(negative)>=ilePerPlik:
                np.random.shuffle(negative)
                np.random.shuffle(positive)
                if len(positive)<len(negative):
                    tmplen=len(positive)
                else:
                    tmplen =len(negative)
                for g in range(tmplen):
                    czesci.append(positive[g])
                    result.append(1)
                    czesci.append(negative[g])
                    result.append(0)
                folder='segments/'+q+'_'+typ
                if not os.path.exists(folder):
                    os.makedirs(folder)
                folder='labels/'+q+'_'+typ
                if not os.path.exists(folder):
                    os.makedirs(folder)
                np.savez_compressed('segments/'+q+'_'+typ+'/' + str(fileCounter), np.array(czesci))
                np.savez_compressed('labels/'+q+'_'+typ+'/' + str(fileCounter), np.array(result))
                czesci = []
                result = []
                positive = []
                negative = []
                fileCounter+=1
    np.random.shuffle(negative)
    np.random.shuffle(positive)
    if len(positive) < len(negative):
        tmplen = len(positive)
    else:
        tmplen = len(negative)
    for g in range(tmplen):
        czesci.append(positive[g])
        result.append(1)
        czesci.append(negative[g])
        result.append(0)
    folder = 'segments/' + q + '_' + typ
    if not os.path.exists(folder):
        os.makedirs(folder)
    folder = 'labels/' + q + '_' + typ
    if not os.path.exists(folder):
        os.makedirs(folder)
    np.savez_compressed('segments/' + q + '_' + typ + '/' + str(fileCounter), np.array(czesci))
    np.savez_compressed('labels/' + q + '_' + typ + '/' + str(fileCounter), np.array(result))


def toGrey(image,whichChannel):
    result=[]
    for i in range(len(image)):
        segment=[]
        for j in range(len(image[whichChannel])):
            segment.append(image[i][j][whichChannel]/255)
        result.append(segment)
    return result




if __name__ == '__main__':
    for i in range(1, 16):
        for j in ['dr', 'h', 'g']:
            myZero = '0'
            if i >= 10:
                myZero = ""
            q=myZero + str(i)
            mask = imread('masks/' + q + '_' + j + '_mask.tif', as_grey=True)
            image = imread('images/'+q+'_'+j+'.jpg')
            image = toGrey(image, 1)
            image = np.array(image)
            image = exposure.equalize_adapthist(image, clip_limit=0.03)
            result = imread('results/'+q+'_'+j+'.tif')
            podzialNaCzesci(image, result, mask,q,j,27)
