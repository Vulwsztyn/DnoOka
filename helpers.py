import numpy as np


def poprawnoscWyniku(wynik, wzor):
    if wynik.shape != wzor.shape:
        raise ValueError("Wzór i wynik mają różne wymiary")
    poprawnosc = wzor.shape[0] * wzor.shape[1]
    for i in range(wzor.shape[0]):
        for j in range(wzor.shape[1]):
            if wzor[i][j] != wynik[i][j]:
                poprawnosc -= 1
    return poprawnosc / (wzor.shape[0] * wzor.shape[1])

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
