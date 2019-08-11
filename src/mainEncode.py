import cv2
import numpy as np
import SteganographyMethod.Grayscale.LsbGray as lg

def main():
    img = cv2.imread('../img/rem.jpg')
    message = "In Syaa Allah lulus 3 semester. Aamiin"
    imgResult = lg.lsbGrayEncryption(img, message)
    cv2.imwrite('../img/stegoLsb.png',imgResult)
    print("Proses Encoding Selesai")

if __name__ == "__main__":
    main()