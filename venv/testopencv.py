# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt


def red_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 赤色のHSVの値域1
    hsv_min = np.array([0, 200, 200])
    hsv_max = np.array([30, 255, 255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2
    hsv_min = np.array([150, 200, 200])
    hsv_max = np.array([179, 255, 255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1 + mask2

def gravity_center(img):
    mu = cv2.moments(img, False)
    print(mu["m00"])
    if mu["m00"] == 0 :
        print("Not fund")
        return
    else :
        x, y = (mu["m10"] / mu["m00"]), (mu["m01"] / mu["m00"])

        #cv2.circle(img, (int(x), int(y)), 4, 100, 2, 4)
        ##plt.imshow(img)
        ##plt.colorbar()
        ##plt.show()

        print(x, y)

def main():
    # カメラのキャプチャ
    cap = cv2.VideoCapture(1)

    while (cap.isOpened()):
        # フレームを取得
        ret, frame = cap.read()

        # 赤色検出
        mask = red_detect(frame)

        # 結果表示
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        gravity_center(mask)

        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()