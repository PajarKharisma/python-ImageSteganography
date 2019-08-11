import cv2
import numpy as np
import SteganographyMethod.Grayscale.LsbGray as lg

def main():
    img = cv2.imread('../img/stegoLsb.png')
    print("Hasil Decode : " + lg.decode(img))

if __name__ == "__main__":
    main()