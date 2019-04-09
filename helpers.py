import numpy as np


def poprawnoscWyniku(wynik, wzor):
    if wynik.shape != wzor.shape:
        raise ValueError("Wzór i wynik mają różne wymiary")
    tp=fp=tn=fn=0
    for i in range(wzor.shape[0]):
        for j in range(wzor.shape[1]):
            if wzor[i][j]==1:
                if wynik[i][j] == 1:
                    tp+=1
                else:
                    fn+=1
            else:
                if wynik[i][j]==1:
                    fp+=1
                else:
                    fn+=1
    accuracy=(tp+tn)/(tp+tn+fp+fn)
    sensitivity = tp/(tp+fn)
    specificity = tn/(tn+fp)
    return accuracy,sensitivity,specificity

def podzialNaCzesci(img,n=9):
    if n%2==0:
        raise ValueError("Wymiar maski ma być nieparzysty")
    margines=n//2
    czesci=[]
    for i in range(margines,img.shape[0]-margines):
        for j in range(margines, img.shape[1] - margines):
            czesc=[]
            for a in range(-margines,n-margines,1):
                wiersz=[]
                for b in range(-margines,n-margines,1):
                    wiersz.append(img[i+a][j+b])
                czesc.append(wiersz)
            czesci.append(czesc)
    return czesci
