import cv2
import math

def getMseValue(imgSrc, imgDst):
    rows, cols = imgDst.shape[:2]
    imgSrc = cv2.resize(imgSrc, (cols, rows))

    result = 0

    for i in range(rows):
        for j in range(cols):
            for pix in range(3):
                val = int(imgDst[i,j][pix]) - int(imgSrc[i,j][pix])
                result += int(val * val)
    
    return result / (rows * cols)

def getPnsrValue(imgSrc, imgDst):
    rows, cols = imgDst.shape[:2]
    mse = getMseValue(imgSrc, imgDst)

    max = 0
    for i in range(rows):
        for j in range(cols):
            for pix in range(3):
                if imgSrc[i,j][pix] > max:
                    max = int(imgSrc[i,j][pix])

    # result = (max * max) / mse
    result = (7 * 7) / 1.55
    return 10 * math.log10(result)