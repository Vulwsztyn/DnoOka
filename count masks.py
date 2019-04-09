import numpy as np
import warnings
import keras

from skimage.io import imread, imsave
for i in range(10,16):
    for j in ['dr','h','g']:
        myZero='0'
        if i>=10:
            myZero=""
        result=imread('masks/'+myZero+str(i)+'_'+j+'_mask.tif',as_grey=True)

        print(result[0][0])
        print(result[1000][1000])
        # suma=0
        # for k in range(result.shape[0]):
        #     for l in range(result.shape[1]):
        #         if np.any(result[k][l]>0):
        #             suma+=1
        # print(myZero + str(i) + '_' + j + '_mask')
        # print(suma)
        # print(result.shape[0]*result.shape[1])
        break
    break

a="""01_dr_mask
6912991
8185344
01_h_mask
6913783
8185344
01_g_mask
6914403
8185344
02_dr_mask
6915024
8185344
02_h_mask
6914369
8185344
02_g_mask
6915730
8185344
03_dr_mask
6915830
8185344
03_h_mask
6912072
8185344
03_g_mask
6914352
8185344
04_dr_mask
6913398
8185344
04_h_mask
6913012
8185344
04_g_mask
6912845
8185344
05_dr_mask
6912374
8185344
05_h_mask
6912106
8185344
05_g_mask
6913655
8185344
06_dr_mask
6914251
8185344
06_h_mask
6911584
8185344
06_g_mask
6912795
8185344
07_dr_mask
6914936
8185344
07_h_mask
6913172
8185344
07_g_mask
6913258
8185344
08_dr_mask
6913320
8185344
08_h_mask
6912686
8185344
08_g_mask
6913716
8185344
09_dr_mask
6913451
8185344
09_h_mask
6913936
8185344
09_g_mask
6915645
8185344
10_dr_mask
6911549
8185344
10_h_mask
6913259
8185344
10_g_mask
6913722
8185344
11_dr_mask
6911775
8185344
11_h_mask
6914041
8185344
11_g_mask
6913339
8185344
12_dr_mask
6914124
8185344
12_h_mask
6912710
8185344
12_g_mask
6913584
8185344
13_dr_mask
6914013
8185344
13_h_mask
6912464
8185344
13_g_mask
6916614
8185344
14_dr_mask
6914033
8185344
14_h_mask
6910309
8185344
14_g_mask
6915352
8185344
15_dr_mask
6912920
8185344
15_h_mask
6912814
8185344
15_g_mask
6911891
8185344"""

# a=a.split('\n')
# min=1e10
# max=0
# for i in range(len(a)):
#     if i%3==1:
#         q=int(a[i])
#         if q>max:
#             max=q
#         elif q<min:
#             min=q
# print(min,max)

a=6910309
b=6916614
c=288193
print(a/c,b/c)
print(c-a%c,c-b%c)
