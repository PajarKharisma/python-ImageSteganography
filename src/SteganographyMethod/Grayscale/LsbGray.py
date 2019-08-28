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
    # konversi gambar ke grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # proses merubah pesan string menjadi bit
    bitMessage = bo.word2bit(message)

    # mendapatkan panjang pesan setelah dirubah menjadi bit
    bitLenght = len(bitMessage)
    index = 0

    # proses mendapatkan jumlah baris dan kolom
    rows, cols = img.shape[:2]
    
    # inisialisasi image baru tempat pesan akan disimpan
    imgResult = np.zeros((rows, cols,1),np.uint8)*255

    # proses menyisipkan pesan ke dalam gambar denganaturan lsb
    # karena citra grayscale, setiap pixel hanya dapat menampung 1 bit pesan.
    for i in range(rows):
        for j in range(cols):
            color = int(img[i,j])
            if index < bitLenght:
                lsbPixel = bo.int2bit(color)[-1]
                imgResult[i,j] = color + lsbVal(bitMessage[index], lsbPixel)
                index += 1
            else:
                imgResult[i,j] = color
    
    # kombinasi nilai val1, val2, val3 akan menyimpan nilai infromasi panjang pesan.
    # Nilai ini dibutuhkan ketika proses decode
    val1, val2, val3 = cl.setCharLength(len(message))

    # ketiga nilai tersebut akan disimpan pada 3 pixel terakhir
    imgResult[rows-1, cols-1] = val1
    imgResult[rows-1, cols-2] = val2
    imgResult[rows-1, cols-3] = val3

    return imgResult

def decode(img):
    # konversi gambar ke grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # proses mendapatkan resolusi gambar
    rows, cols = img.shape[:2]

    # proses mendapatkan nilai panjang pesan. Sehingga proses extraksi akan berhenti ketika semua pesan sudah diextract
    charLength = cl.getCharLenth(img[rows-1, cols-1], img[rows-1, cols-2], img[rows-1, cols-3])

    # panjang karakter dikalikan dengan 8 karena 1 karakter = 8 bit integer
    charLength = charLength * 8
    index = 0
    bit = []
    toogle = True
    
    # proses extraksi pesan dengan cara menelusuri setiap pixel pada gambar
    # proses menelusuri akan berhenti ketika semua pesan sudah diextract
    for i in range(rows):
        for j in range(cols):
            if index < charLength:
                if int(img[i,j]) % 2 == 0:
                    bit.append('0') 
                else:
                    bit.append('1')
                index += 1
                if toogle:
                    img[i,j] = 255
                    toogle = False
                else:
                    img[i,j] = 0
                    toogle = True
                # img[i,j] += 1
                # if img[i,j] > 255:
                #     img[i,j] = 255
            else:
                break
    cv2.imwrite('../img/stegoLsbGray.png',img)
    return bo.bit2word(bit)