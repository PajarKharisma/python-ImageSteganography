import cv2
import math

# fungsi untuk menghitung nilai MSE
def getMseValue(imgSrc, imgDst, mode):
    rows, cols = imgDst.shape[:2]
    imgSrc = cv2.resize(imgSrc, (cols, rows))

    result = 0

    if mode == 0:
        for i in range(rows):
            for j in range(cols):
                for pix in range(3):
                    val = int(imgDst[i,j][pix]) - int(imgSrc[i,j][pix])
                    result += int(val * val)
        
        return result / ((rows * cols) * 3)
    else:
        imgSrc = cv2.cvtColor(imgSrc, cv2.COLOR_BGR2GRAY)
        imgDst = cv2.cvtColor(imgDst, cv2.COLOR_BGR2GRAY)

        for i in range(rows):
            for j in range(cols):
                val = int(imgDst[i,j]) - int(imgSrc[i,j])
                result += int(val * val)
        
        return result / (rows * cols)

# fungsi untuk menghitung nilai PNSR
def getPnsrValue(imgSrc, imgDst, mode):
    rows, cols = imgDst.shape[:2]
    mse = getMseValue(imgSrc, imgDst, mode)

    max = 0

    if mode == 0:
        for i in range(rows):
            for j in range(cols):
                for pix in range(3):
                    if imgSrc[i,j][pix] > max:
                        max = int(imgSrc[i,j][pix])
    else:
        imgSrc = cv2.cvtColor(imgSrc, cv2.COLOR_BGR2GRAY)
        imgDst = cv2.cvtColor(imgDst, cv2.COLOR_BGR2GRAY)
        for i in range(rows):
            for j in range(cols):
                if imgSrc[i,j] > max:
                    max = int(imgSrc[i,j])

    result = (max * max) / mse
    return 10 * math.log10(result)