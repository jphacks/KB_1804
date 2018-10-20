# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
from wheel_control import WheelControl
import RPi.GPIO as GPIO
import time

class OpenCV:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.width = cap.get(3)
        self.height = cap.get(4)

    def red_detect(self, img):
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

    def gravity_center(self, img):
        mu = cv2.moments(img, False)
        ##print(mu["m00"])
        area = mu["m00"]
        ##print(area)
        if mu["m00"] == 0:
            # ＃# print("Not fund")
            return "Wait"
        elif area / 100 > (self.width * self.height) / 2:
            return "Back"
        else:
            x, y = (mu["m10"] / mu["m00"]), (mu["m01"] / mu["m00"])

            # cv2.circle(img, (int(x), int(y)), 4, 100, 2, 4)
            ##plt.imshow(img)
            ##plt.colorbar()
            ##plt.show()

            # print(x, y)
            if x < 300:
                return "Left"
            elif 300 <= x < 500:
                return "Forward"
            elif 500 <= x:
                return "Right"

    def main(self):

        while (self.cap.isOpened()):
            # フレームを取得
            ret, frame = cap.read()

            # 赤色検出
            mask = red_detect(frame)

            # 結果表示
            cv2.imshow("Frame", frame)
            cv2.imshow("Mask", mask)
            command = gravity_center(mask)

            if command != None:
                print(command)
                try:
                    wc = WheelControl()
                    if(command == "Foward"):
                        wc.forward(duty=100)
                        time.sleep(1)
                    elif(command == "Back"):
                        wc.backward(duty=100)
                        time.sleep(1)
                    elif(command == "Left"):
                        wc.rotate_left(duty=50)
                        time.sleep(1)
                    elif(command == "Rigth"):
                        wc.rotate_right(duty=50)
                        time.sleep(1)
                    elif(command == "Wait"):
                        wc.stop()

                    print("done")

                finally:
                    print("fin")

                # qキーが押されたら途中終了
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

