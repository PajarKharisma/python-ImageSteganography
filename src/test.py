import cv2
import numpy as np
import math

# module yg dibuat sendiri
import SubProcess.Measurement as msr
import SteganographyMethod.Grayscale.PvdGray as pg
import SteganographyMethod.Grayscale.MfGray as mg
import SubProcess.BitOperation as bo

pesan = 'a'
pesanBit = bo.word2bit(pesan)
print('Isi pesan : ', pesan, ' | Setelah dikonversi menjadi bit : ', pesanBit)
img = np.array([
    [234, 120, 187, 192],
    [89, 24, 5, 163],
    [192, 27, 9, 120],
    [77, 44, 6, 180]
])

print('\nnilai matrix sebelum encode : ')
for i in range(4):
    for j in range(4):
        print(img[i,j],'\t', end = ' ')
    print()

imgResult = mg.encode(img, pesan, False)
print('\nnilai matrix setelah encode : ')
for i in range(4):
    for j in range(4):
        print(imgResult[i,j],'\t', end = ' ')
    print()
# cv2.waitKey(0)

# print(math.log2(32))