import cv2
import numpy as np
import SteganographyMethod.Grayscale.LsbGray as lg
import SteganographyMethod.Grayscale.PvdGray as pg
import SteganographyMethod.Color.LsbColor as lc

def main():
    # LSB GRAY
    # img = cv2.imread('../img/stegoLsbGray.png')
    # print("Hasil Decode : " + lg.decode(img))

    # PVD GRAY
    # img = cv2.imread('../img/stegoPvdGray.png')
    # print("Hasil Decode : " + pg.decode(img))

    # LSB COLOR
    img = cv2.imread('../img/stegoLsbColor.png')
    print("Hasil Decode : " + lc.decode(img))

if __name__ == "__main__":
    main()