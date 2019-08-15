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

def encode(img, message):
    bitMessage = bo.word2bit(message)
    bitLenght = len(bitMessage)
    index = 0

    rows, cols = img.shape[:2]
    imgResult = np.zeros((rows, cols,3),np.uint8)*255
    lastIteration = True
    for i in range(rows):
        for j in range(cols):
            color = img[i,j]
            if lastIteration:
                for pix in range(3):
                    if index < bitLenght:
                        lsbPixel = bo.int2bit(color[pix])[-1]
                        newPixVal = color[pix] + lsbVal(bitMessage[index], lsbPixel)
                        if newPixVal < 0:
                            newPixVal = 1
                        if newPixVal > 255:
                            newPixVal = 254
                        imgResult[i,j][pix] = newPixVal
                        index += 1
                    else:
                        lastIteration = False
            else:
                imgResult[i,j] = color
    
    val1, val2, val3 = cl.setCharLength(len(message))
    imgResult[rows-1, cols-1] = [val1, val2, val3]

    return imgResult

def decode(img):
    rows, cols = img.shape[:2]
    charLength = cl.getCharLenth(img[rows-1, cols-1][0], img[rows-1, cols-1][1], img[rows-1, cols-1][2])
    charLength = charLength * 8
    index = 0
    bit = []
    lastIteration = True
    for i in range(rows):
        for j in range(cols):
            if lastIteration:
                for pix in range(3):
                    if index < charLength:
                        if int(img[i,j][pix]) % 2 == 0:
                            bit.append('0')
                        else:
                            bit.append('1')
                        index += 1
                    else:
                        lastIteration = False

                    img[i,j][pix] += 1
                    if img[i,j][pix] > 255:
                        img[i,j][pix] = 255
            else:
                break

    cv2.imwrite('../img/stegoLsbColor.png',img)
    return bo.bit2word(bit)