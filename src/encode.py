# module yg disediakan python
import cv2
import numpy as np

# module yg dibuat sendiri
import SubProcess.Measurement as msr
import SteganographyMethod.Grayscale.LsbGray as lg
import SteganographyMethod.Grayscale.PvdGray as pg
import SteganographyMethod.Grayscale.MfGray as mg
import SteganographyMethod.Color.LsbColor as lc
import SteganographyMethod.Color.PvdColor as pc
import SteganographyMethod.Color.MfColor as mc

def main():
    # load gambar
    img = cv2.imread('../img/rem.jpg')

    # load pesan
    message = open("../msg/message.txt", "r").read()

    # imgResult, gambar hasil encode
    # imwrite, fungsi untuk menyimpan gambar hasil encode

    # mode 1 untuk gambar grayscale, mode 0 untuk gambar berwarna

    # LSB GRAY
    # path = '../img/lsb-gray/after-encode.png'
    # mode = 1
    # imgResult = lg.encode(img, message)
    # cv2.imwrite(path, imgResult)
    # print("Proses encoding citra grayscale dengan metode Least Significant Bit selesai")

    # PVD GRAY
    # path = '../img/pvd-gray/after-encode.png'
    # mode = 1
    # imgResult = pg.encode(img, message)
    # cv2.imwrite(path, imgResult)
    # print("Proses encoding citra grayscale dengan metode Pixel Value Difference selesai")

    # MF GRAY
    # path = '../img/mf-gray/after-encode.png'
    # mode = 1
    # imgResult = mg.encode(img, message)
    # cv2.imwrite(path, imgResult)
    # print("Proses encoding citra grayscale dengan metode Modulus Function selesai")

    # LSB COLOR
    # path = '../img/lsb-color/after-encode.png'
    # mode = 0
    # imgResult = lc.encode(img, message)
    # cv2.imwrite(path, imgResult)
    # print("Proses encoding citra color dengan metode Least Significant Bit selesai")

    # PVD COLOR
    # path = '../img/pvd-color/after-encode.png'
    # mode = 0
    # imgResult = pc.encode(img, message)
    # cv2.imwrite(path, imgResult)
    # print("Proses encoding citra color dengan metode Pixel Value Difference selesai")


    # MF COLOR
    path = '../img/mf-color/after-encode.png'
    mode = 0
    imgResult = mc.encode(img, message)
    cv2.imwrite(path, imgResult)
    print("Proses encoding citra color dengan metode Modulus Function selesai")

    imgDst = cv2.imread(path)
    print("Nilai MSE : %0.3f" % (msr.getMseValue(img, imgDst, mode)))
    print("Nilai PNSR : %0.3f" % (msr.getPnsrValue(img, imgDst, mode)))

if __name__ == "__main__":
    main()