import cv2
import numpy as np
import SteganographyMethod.Grayscale.LsbGray as lg
import SteganographyMethod.Grayscale.PvdGray as pg
import SteganographyMethod.Color.LsbColor as lc

def main():
    img = cv2.imread('../img/rem.jpg')
    message = "In Syaa Allah lulus 3 semester.."

    # LSB GRAY
    # imgResult = lg.encode(img, message)
    # cv2.imwrite('../img/stegoLsbGray.png',imgResult)
    # print("Proses Encoding Selesai")

    # PVD GRAY
    # imgResult = pg.encode(img, message)
    # cv2.imwrite('../img/stegoPvdGray.png', imgResult)
    # print("Proses Encoding Selesai")

    imgResult = lc.encode(img, message)
    cv2.imwrite('../img/stegoLsbColor.png',imgResult)
    print("Proses Encoding Selesai")

if __name__ == "__main__":
    main()