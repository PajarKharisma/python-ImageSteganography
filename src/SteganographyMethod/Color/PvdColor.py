# module yg disediakan python
import numpy as np
import cv2
import math

# module yg dibuat sendiri
import SubProcess.BitOperation as bo
import SteganographyMethod.CharLength as cl

# fungsi mendapatkan nilai dari tabel kuantisasi
def qTable(val):
    if val in range(0,8):
        return 0, 3
    elif val in range(8,16):
        return 8, 3
    elif val in range(16,32):
        return 16, 3
    elif val in range(32,64):
        return 32, 3
    elif val in range(64,128):
        return 64, 3
    elif val in range(128,256):
        return 128, 3

# fungsi encode pesan
def encode(img, message):
    # proses merubah pesan string menjadi bit
    bitMessage = bo.word2bit(message)

    # mendapatkan panjang pesan setelah dirubah menjadi bit
    bitLenght = len(bitMessage)
    index = 0

    # proses mendapatkan jumlah baris dan kolom
    rows, cols = img.shape[:2]
    if rows % 2 == 1:rows += 1
    if cols % 2 == 1:cols += 1
    img = cv2.resize(img, (cols, rows))

    # inisialisasi image baru tempat pesan akan disimpan
    imgResult = np.zeros((rows, cols,3),np.uint8)*255
    lastIteration = True
    isFinish = True

    # proses menyisipkan pesan ke dalam gambar dengan aturan modulus function
    # karena citra berwarna, setiap pixel dapat menampung minimal 3 bit pesan. Setiap bit disisipkan dalam chanel R, G, dan B
    for i in range(rows):
        j = 0
        while j < cols:
            color = img[i,j]
            if lastIteration:
                for pix in range(3):
                    if isFinish:
                        gi, gi1 = int(img[i,j][pix]), int(img[i,j+1][pix])
                        diff = gi1 - gi
                        ik, n = qTable(abs(diff))
                        restBit = len(bitMessage)
                        if restBit <= n:
                            bitMessage.extend([0 for i in range(n - restBit)])
                            lastIteration = False
                            isFinish = False
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

                        imgResult[i,j][pix] = gi
                        imgResult[i,j+1][pix] = gi1
                j += 2
            else:
                imgResult[i,j] = color
                j += 1
    
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

    # proses extraksi pesan dengan cara menelusuri setiap pixel pada gambar
    # proses menelusuri akan berhenti ketika semua pesan sudah diextract
    for i in range(rows):
        j = 0
        while j < cols:
            if lastIteration:
                for pix in range(3):
                    if index < charLength:
                        gi, gi1 = int(img[i,j][pix]), int(img[i,j+1][pix])
                        diff = abs(gi - gi1)
                        ik, n = qTable(diff)
                        b = bo.int2bit(abs(diff - ik))
                        fixBit = [0 for i in range(n - len(b))]
                        fixBit.extend(b)
                        bit.extend(fixBit)
                        index += n
                        img[i,j][pix] -= diff
                        if img[i,j][pix] < 0:
                            img[i,j][pix] = 0
                    else:
                        lastIteration = False
            else:
                break
            j += 2

    cv2.imwrite('../img/pvd-color/after-decode.png',img)
    return bo.bit2word(bit)