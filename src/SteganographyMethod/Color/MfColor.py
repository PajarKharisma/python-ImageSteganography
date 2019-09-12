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
        return 16, 4
    elif val in range(32,64):
        return 32, 5
    elif val in range(64,128):
        return 64, 6
    elif val in range(128,256):
        return 128, 7

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
                        diff = abs(gi - gi1)
                        ik, n = qTable(abs(diff))
                        restBit = len(bitMessage)
                        if restBit <= n:
                            bitMessage.extend([0 for i in range(n - restBit)])
                            lastIteration = False
                            isFinish = False
                        bit = bitMessage[:n]
                        del bitMessage[:n]
                        b = bo.bit2int(bit)

                        r = (gi + gi1) % math.pow(2,n)
                        m = abs(r - b)
                        m1 = abs(math.pow(2,n) - m)

                        if (r > b) and (m <= math.pow(2,n)/2) and (gi >= gi1):
                            gi -= math.ceil(m/2)
                            gi1 -= math.floor(m/2)
                        elif (r > b) and (m <= math.pow(2,n)/2) and (gi < gi1):
                            gi -= math.ceil(m/2)
                            gi1 -= math.floor(m/2)
                        elif (r > b) and (m > math.pow(2,n)/2) and (gi >= gi1):
                            gi += math.ceil(m1/2)
                            gi1 += math.floor(m1/2)
                        elif (r > b) and (m > math.pow(2,n)/2) and (gi < gi1):
                            gi += math.ceil(m1/2)
                            gi1 += math.floor(m1/2)
                        elif (r <= b) and (m <= math.pow(2,n)/2) and (gi >= gi1):
                            gi += math.ceil(m/2)
                            gi1 += math.floor(m/2)
                        elif (r <= b) and (m <= math.pow(2,n)/2) and (gi < gi1):
                            gi += math.ceil(m/2)
                            gi1 += math.floor(m/2)
                        elif (r <= b) and (m > math.pow(2,n)/2) and (gi >= gi1):
                            gi -= math.ceil(m1/2)
                            gi1 -= math.floor(m1/2)
                        elif (r <= b) and (m > math.pow(2,n)/2) and (gi < gi1):
                            gi -= math.ceil(m1/2)
                            gi1 -= math.floor(m1/2)

                        po1 = img[i,j][pix]
                        po2 = img[i,j+1][pix]
                        if (po1 == 0 or po2 == 0) and (gi < 0 or gi1 < 0):
                            gi += math.pow(2,n)
                            gi1 += math.pow(2,n)
                            img[i,j][pix] = gi
                            img[i,j+1][pix] = gi1
                        elif (po1 == 255 or po2 == 255) and (gi > 255 or gi1 > 255):
                            gi -= math.pow(2,n)
                            gi1 -= math.pow(2,n)
                            img[i,j][pix] = gi
                            img[i,j+1][pix] = gi1
                        elif diff > 128:
                            if gi < 0 and gi1 >= 0:
                                img[i,j][pix] = 0
                                img[i,j+1][pix] = gi + gi1
                            elif gi >= 0 and gi1 < 0:
                                img[i,j][pix] = gi + gi1
                                img[i,j+1][pix] = 0
                            elif gi > 255 and gi1 >= 0:
                                img[i,j][pix] = 255
                                img[i,j+1][pix] = gi1 + (gi - 255)
                            elif gi >= 0 and gi1 >255:
                                img[i,j][pix] = gi + (gi1 - 255)
                                img[i,j+1][pix] = 255
                        else:
                            imgResult[i,j][pix] = gi
                            imgResult[i,j+1][pix] = gi1
                j += 2
            else:
                imgResult[i,j] = color
                j += 1
    
    # kombinasi nilai val1, val2, val3 akan menyimpan nilai infromasi panjang pesan.
    # Nilai ini dibutuhkan ketika proses decode
    val1, val2, val3 = cl.setCharLength(len(message))

    # ketiga nilai tersebut akan disimpan pada pixel terakhir
    imgResult[rows-1, cols-1] = [val1, val2, val3]

    return imgResult

def decode(img):
    # proses mendapatkan resolusi gambar
    rows, cols = img.shape[:2]

    # proses mendapatkan nilai panjang pesan. Sehingga proses extraksi akan berhenti ketika semua pesan sudah diextract
    charLength = cl.getCharLenth(img[rows-1, cols-1][0], img[rows-1, cols-1][1], img[rows-1, cols-1][2])

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
                        b = bo.int2bit(int((gi + gi1) % math.pow(2,n)))
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
    
    cv2.imwrite('../img/mf-color/after-decode.png',img)
    return bo.bit2word(bit)