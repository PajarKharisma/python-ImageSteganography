import cv2
import numpy as np
import SteganographyMethod.Grayscale.LsbGray as lg
import SteganographyMethod.Grayscale.PvdGray as pg

def main():
    # LSB
    # img = cv2.imread('../img/stegoLsb.png')
    # print("Hasil Decode : " + lg.decode(img))

    # PVD
    img = cv2.imread('../img/stegoPvd.png')
    print("Hasil Decode : " + pg.decode(img))

if __name__ == "__main__":
    main()