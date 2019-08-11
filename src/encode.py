import cv2
import numpy as np
import SteganographyMethod.Grayscale.LsbGray as lg
import SteganographyMethod.Grayscale.PvdGray as pg

def main():
    img = cv2.imread('../img/rem.jpg')
    message = "In Syaa Allah lulus"

    # LSB
    # imgResult = lg.encode(img, message)
    # cv2.imwrite('../img/stegoLsb.png',imgResult)
    # print("Proses Encoding Selesai")

    # PVD
    imgResult = pg.encode(img, message)
    cv2.imwrite('../img/stegoPvd.png', imgResult)
    print("Proses Encoding Selesai")

    # src = cv2.imread('../img/rem.jpg', 0)
    # dest = cv2.imread('../img/stegoPvd.png', 0)
    # pg.test(src, dest, message)

if __name__ == "__main__":
    main()