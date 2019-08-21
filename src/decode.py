import cv2
import numpy as np
import SteganographyMethod.Grayscale.LsbGray as lg
import SteganographyMethod.Grayscale.PvdGray as pg
import SteganographyMethod.Grayscale.MfGray as mg
import SteganographyMethod.Color.LsbColor as lc
import SteganographyMethod.Color.PvdColor as pc
import SteganographyMethod.Color.MfColor as mc

def main():
    # LSB GRAY
    # img = cv2.imread('../img/stegoLsbGray.png')
    # print("Hasil Decode : " + lg.decode(img))

    # PVD GRAY
    # img = cv2.imread('../img/stegoPvdGray.png')
    # print("Hasil Decode : " + pg.decode(img))

    # MF GRAY
    # img = cv2.imread('../img/stegoMfGray.png')
    # print("Hasil Decode : " + mg.decode(img))

    # LSB COLOR
    # img = cv2.imread('../img/stegoLsbColor.png')
    # print("Hasil Decode : " + lc.decode(img))

    # PVD COLOR
    # img = cv2.imread('../img/stegoPvdColor.png')
    # print("Hasil Decode : " + pc.decode(img))

    # MF COLOR
    img = cv2.imread('../img/stegoMfColor.png')
    print("Hasil Decode : " + mc.decode(img))

if __name__ == "__main__":
    main()