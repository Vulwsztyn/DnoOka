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
    for i in range(margines, img.shape[0] - margines):
        # print('i',i)
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
            fileCounter+=1
    i=-1
    while len(czesci)<ilePerPlik:
        czesci.append(czesci[i])
        result.append(result[i])
        i-=1
    np.savez_compressed('segments/'+q+'_'+typ+'/' + str(fileCounter), np.array(czesci))
    np.savez_compressed('labels/'+q+'_'+typ+'/' + str(fileCounter), np.array(result))


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
            p1, p2 = np.percentile(image, (10, 100))
            image = exposure.rescale_intensity(image, in_range=(p1, p2))
            result = imread('results/'+q+'_'+j+'.tif')
            podzialNaCzesci(image, result, mask,q,j,9)
