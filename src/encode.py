import cv2
import numpy as np
import SteganographyMethod.Grayscale.LsbGray as lg
import SteganographyMethod.Grayscale.PvdGray as pg
import SteganographyMethod.Grayscale.MfGray as mg
import SteganographyMethod.Color.LsbColor as lc
import SteganographyMethod.Color.PvdColor as pc
import SteganographyMethod.Color.MfColor as mc

def main():
    img = cv2.imread('../img/rem.jpg')
    message = open("../msg/message.txt", "r").read()

    # LSB GRAY
    # imgResult = lg.encode(img, message)
    # cv2.imwrite('../img/stegoLsbGray.png',imgResult)
    # print("Proses Encoding Selesai")

    # PVD GRAY
    # imgResult = pg.encode(img, message)
    # cv2.imwrite('../img/stegoPvdGray.png', imgResult)
    # print("Proses Encoding Selesai")

    # MF GRAY
    # imgResult = mg.encode(img, message)
    # cv2.imwrite('../img/stegoMfGray.png', imgResult)
    # print("Proses Encoding Selesai")

    # LSB COLOR
    # imgResult = lc.encode(img, message)
    # cv2.imwrite('../img/stegoLsbColor.png',imgResult)
    # print("Proses Encoding Selesai")

    # PVD COLOR
    # imgResult = pc.encode(img, message)
    # cv2.imwrite('../img/stegoPvdColor.png',imgResult)
    # print("Proses Encoding Selesai")

    # MF COLOR
    imgResult = mc.encode(img, message)
    cv2.imwrite('../img/stegoMfColor.png',imgResult)
    print("Proses Encoding Selesai")

if __name__ == "__main__":
    main()