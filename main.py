import numpy as np
import warnings
import keras
warnings.filterwarnings("ignore")
from skimage.io import imread, imsave

def podzialNaCzesci(img,res,n=9):
    if n%2==0:
        raise ValueError("Wymiar maski ma być nieparzysty")
    margines=n//2
    czesci=[]
    counter=0
    result=[]
    for i in range(margines,img.shape[0]-margines):
        print(i-margines,' out of ',img.shape[0]-margines-margines)
        for j in range(margines, img.shape[1] - margines):
            czesc=[]
            for a in range(-margines,n-margines,1):
                wiersz=[]
                for b in range(-margines,n-margines,1):
                    wiersz.append(img[i+a][j+b])
                czesc.append(wiersz)
            if np.average(czesc)>0.1:
                result.append(res[i][j])
                czesci.append(czesc)
        if (i-margines)%100==0 and (i-margines)!=0:
            np.savez_compressed('segments/01_h/'+str(counter),np.array(czesci))
            np.savez_compressed('labels/01_h/' + str(counter), np.array(result))
            czesci=[]
            result=[]
            counter = counter + 1
            # czesci=[]
    np.savez_compressed('segments/01_h/' + str(counter), np.array(czesci))
    np.savez_compressed('labels/01_h/' + str(counter), np.array(result))

def toGrey(image,whichChannel):
    for i in range(len(image)):
        for j in range(len(image[whichChannel])):
            image[i][j]=image[i][j][whichChannel]
    return image


# print("reading")
# image=imread('images/01_h.jpg',as_gray=True)
# result=imread('results/01_h.tif')
#
# print("podzieling")
# podzialNaCzesci(image,result,9)

train_images=np.load('segments/01_h/0.npz')['arr_0']
train_labels=np.load('labels/01_h/0.npz')['arr_0']/255
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(9, 9)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(1, activation='softmax')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=1)