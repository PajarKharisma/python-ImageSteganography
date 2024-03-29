# module yg disediakan python
import numpy as np
import cv2

# module yg dibuat sendiri
import SubProcess.BitOperation as bo
import SteganographyMethod.CharLength as cl

# fungsi mendapatkan nilai bit
def lsbVal(a, b):
    result = 0
    if a == b:
        result = 0
    elif a == 1 and b == 0:
        result = 1
    elif a == 0 and b == 1:
        result = - 1

    return result

# fungsi encode pesan
def encode(img, message):
    # proses merubah pesan string menjadi bit
    bitMessage = bo.word2bit(message)

    # mendapatkan panjang pesan setelah dirubah menjadi bit
    bitLenght = len(bitMessage)
    index = 0

    # proses mendapatkan jumlah baris dan kolom
    rows, cols = img.shape[:2]

    # inisialisasi image baru tempat pesan akan disimpan
    imgResult = np.zeros((rows, cols,3),np.uint8)*255
    lastIteration = True

    # proses menyisipkan pesan ke dalam gambar denganaturan lsb
    # karena citra berwarna, setiap pixel dapat menampung 3 bit pesan. Setiap bit disimpan dalam chanel R, G, dan B
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
    
    # kombinasi nilai val1, val2, val3 akan menyimpan nilai infromasi panjang pesan.
    # Nilai ini dibutuhkan ketika proses decode
    val1, val2, val3, val4 = cl.setCharLength(len(message))

    # ketiga nilai tersebut akan disimpan pada pixel terakhir
    imgResult[rows-1, cols-1] = [val1, val2, val3]
    imgResult[rows-1, cols-2][0] = val4

    return imgResult

def decode(img):
    # proses mendapatkan resolusi gambar
    rows, cols = img.shape[:2]

    # proses mendapatkan nilai panjang pesan. Sehingga proses extraksi akan berhenti ketika semua pesan sudah diextract
    charLength = cl.getCharLenth(img[rows-1, cols-1][0], img[rows-1, cols-1][1], img[rows-1, cols-1][2], img[rows-1, cols-2][0])
    
    # panjang karakter dikalikan dengan 8 karena 1 karakter = 8 bit integer
    charLength = charLength * 8
    index = 0
    bit = []
    lastIteration = True
    toogle = True

    # proses extraksi pesan dengan cara menelusuri setiap pixel pada gambar
    # proses menelusuri akan berhenti ketika semua pesan sudah diextract
    for i in range(rows):
        for j in range(cols):
            if lastIteration:
                for pix in range(3):
                    if index < charLength:
                        if int(img[i,j][pix]) % 2 == 0:
                            bit.append('0')
                            img[i,j][pix] += 1
                        else:
                            bit.append('1')
                            img[i,j][pix] -= 1
                        index += 1

                        if img[i,j][pix] < 0:
                            img[i,j][pix] = 0
                        if img[i,j][pix] > 255:
                            img[i,j][pix] = 255
                    else:
                        lastIteration = False
            else:
                break

    cv2.imwrite('../img/lsb-color/after-decode.png',img)
    return bo.bit2word(bit)