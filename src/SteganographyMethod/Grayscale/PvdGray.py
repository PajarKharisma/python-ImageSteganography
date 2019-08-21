import SubProcess.BitOperation as bo
import SteganographyMethod.CharLength as cl
import numpy as np
import cv2
import math

def qTable(val):
    if val in range(0,8):
        return 0, 3
    elif val in range(8,16):
        return 8, 3
    elif val in range(16,32):
        return 16, 4
    elif val in range(32,64):
        return 32, 5
    elif val in range(64,128):
        return 64, 6
    elif val in range(128,256):
        return 128, 7

def encode(img, message):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bitMessage = bo.word2bit(message)
    bitLenght = len(bitMessage)
    index = 0

    rows, cols = img.shape[:2]
    if rows % 2 == 1:rows += 1
    if cols % 2 == 1:cols += 1
    img = cv2.resize(img, (cols, rows))

    imgResult = np.zeros((rows, cols,1),np.uint8)*255
    lastIteration = True
    isFinish = True
    for i in range(rows):
        j = 0
        while j < cols:
            color = int(img[i,j])
            if lastIteration:
                gi, gi1 = int(img[i,j]), int(img[i,j+1])
                diff = gi1 - gi
                ik, n = qTable(abs(diff))
                restBit = len(bitMessage)
                if restBit <= n:
                    bitMessage.extend([0 for i in range(n - restBit)])
                    lastIteration = False
                bit = bitMessage[:n]
                del bitMessage[:n]
                b = bo.bit2int(bit)

                diffA = 0
                if diff >= 0:
                    diffA = ik + b
                else:
                    diffA = -1 * (ik + b)

                m = abs(diffA - abs(diff))
                if m % 2 == 0:
                    gi -= int(m/2)
                    gi1 += int(m/2)
                    while abs(gi - gi1) != b:
                        if gi < gi1:
                            gi += 1
                        else:
                            gi1 += 1
                else:
                    gi -= math.ceil(m/2)
                    gi1 += math.floor(m/2)
                    while abs(gi - gi1) != b:
                        if gi < gi1:
                            gi += 1
                        else:
                            gi1 += 1
                
                if gi < 0:
                    gi1 -= gi
                    gi = 0

                if gi1 > 255:
                    gi -= gi1 - 255
                    gi1 = 255

                imgResult[i,j] = gi
                imgResult[i,j+1] = gi1
                j += 2
            else:
                imgResult[i,j] = color
                j += 1
    
    val1, val2, val3 = cl.setCharLength(len(message))
    imgResult[rows-1, cols-1] = val1
    imgResult[rows-1, cols-2] = val2
    imgResult[rows-1, cols-3] = val3

    return imgResult

def decode(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows, cols = img.shape[:2]
    charLength = cl.getCharLenth(img[rows-1, cols-1], img[rows-1, cols-2], img[rows-1, cols-3])
    charLength = charLength * 8
    index = 0
    bit = []
    for i in range(rows):
        j = 0
        while j < cols:
            if index < charLength:
                gi, gi1 = int(img[i,j]), int(img[i,j+1])
                diff = abs(gi - gi1)
                ik, n = qTable(diff)
                b = bo.int2bit(abs(diff - ik))
                fixBit = [0 for i in range(n - len(b))]
                fixBit.extend(b)
                bit.extend(fixBit)
                index += n
                img[i,j] = 255
                img[i,j+1] = 0
                # img[i,j] += 1
                # img[i,j+1] -= 1
                # if img[i,j] > 255:
                #     img[i,j] = 255
                # if img[i,j+1] < 0:
                #     img[i,j+1] = 0
            else:
                break
            j += 2

    cv2.imwrite('../img/stegoPvdGray.png', img)
    return bo.bit2word(bit)