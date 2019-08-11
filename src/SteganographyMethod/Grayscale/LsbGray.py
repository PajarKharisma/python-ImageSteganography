import SubProcess.BitOperation as bo
import SteganographyMethod.CharLength as cl
import numpy as np
import cv2


def lsbVal(a, b):
    result = 0
    if a == b:
        result = 0
    elif a == 1 and b == 0:
        result = 1
    elif a == 0 and b == 1:
        result = - 1

    return result

def lsbGrayEncryption(img, message):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bitMessage = bo.word2bit(message)
    bitLenght = len(bitMessage)
    index = 0

    rows, cols = img.shape[:2]
    imgResult = np.zeros((rows, cols,1),np.uint8)*255
    for i in range(rows):
        for j in range(cols):
            color = int(img[i,j])
            if index < bitLenght:
                lsbPixel = bo.int2bit(color)[-1]
                imgResult[i,j] = color + lsbVal(bitMessage[index], lsbPixel)
                index += 1
            else:
                imgResult[i,j] = color
    
    val1, val2, val3 = cl.setCharLength(len(message))
    imgResult[rows-1, cols-1] = val1
    imgResult[rows-1, cols-2] = val2
    imgResult[rows-1, cols-3] = val3

    return imgResult

def lsbGrayExtract(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows, cols = img.shape[:2]
    charLength = cl.getCharLenth(img[rows-1, cols-1], img[rows-1, cols-2], img[rows-1, cols-3])
    charLength = charLength * 8
    index = 0
    bit = []
    for i in range(rows):
        for j in range(cols):
            if index < charLength:
                if int(img[i,j]) % 2 == 0:
                    bit.append('0')
                else:
                    bit.append('1')
                index += 1
            else:
                break
    return bo.bit2word(bit)