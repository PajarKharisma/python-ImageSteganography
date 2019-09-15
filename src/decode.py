# module yg disediakan python
import cv2
import numpy as np

# module yg dibuat sendiri
import SteganographyMethod.Grayscale.LsbGray as lg
import SteganographyMethod.Grayscale.PvdGray as pg
import SteganographyMethod.Grayscale.MfGray as mg
import SteganographyMethod.Color.LsbColor as lc
import SteganographyMethod.Color.PvdColor as pc
import SteganographyMethod.Color.MfColor as mc

def main():
    # untuk melihat pesan dari gambar yang sudah didecode, ganti imgName dengan nama 'after-decode.png'. Pesan di gambar ini sudah dalam keaddan rusak
    # untuk melihat pesan dari gambar yang belum didecode, ganti imgName dengan nama 'after-encode.png'
    imgName = 'after-encode.png'

    # LSB GRAY
    # img = cv2.imread('../img/lsb-gray/%s' % imgName)
    # result = lg.decode(img)

    # PVD GRAY
    # img = cv2.imread('../img/pvd-gray/%s' % imgName)
    # result = pg.decode(img)

    # MF GRAY
    # img = cv2.imread('../img/mf-gray/%s' % imgName)
    # result = mg.decode(img)

    # LSB COLOR
    img = cv2.imread('../img/lsb-color/%s' % imgName)
    result = lc.decode(img)

    # PVD COLOR
    img = cv2.imread('../img/pvd-color/%s' % imgName)
    result = pc.decode(img)

    # MF COLOR
    # img = cv2.imread('../img/mf-color/%s' % imgName)
    # result = mc.decode(img)

    decodeFile = open("../msg/decode-result.txt", "w", encoding='utf-8')
    decodeFile.write(result)
    decodeFile.close()

    print("Hasil Decode : %s" % result)

if __name__ == "__main__":
    main()