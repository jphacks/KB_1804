# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
from wheel_control import WheelControl
import RPi.GPIO as GPIO
import time
from check import ClovaChecker

class DetectAndRun:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.width = 320 # self.cap.get(3)
        self.height = 240 # self.cap.get(4)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        self.dt = 0.05
        #self.wc = None
        # self.wc = WheelControl()
        
        self.dt_check = 5  # Period to check clova. 
        self.cc= ClovaChecker()
        
    def face2command(self, img):
        cascade_path = "./haarcascades/haarcascade_frontalface_default.xml"
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(cascade_path)
        facerects = cascade.detectMultiScale(img_gray,
                                            scaleFactor=1.3,
                                            minNeighbors=5)
        
        x_center = self.width / 2
        print(facerects)
        
        # if facerects != ():
        if len(facerects) == 1:
            
            x, y = facerects[0][0], facerects[0][1]
            w, h = facerects[0][2], facerects[0][3]
            
            face_center = x + w//2
            width_ex = 25

            area_img = self.width * self.height
            
            print("face_center", face_center)

            if face_center < x_center - width_ex:
                command = "L"
            elif face_center > x_center + width_ex:
                command = "R"
            elif w * h > area_img * 0.2:
                command = "B"
            elif w * h < area_img * 0.2:
                command = "F"
            else:
                command =" W"
        else:
            command = "W"
        
        
        return command

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
            return "W"
        elif area / 100 > (self.width * self.height) / 2:
            return "B"
        else:
            x, y = (mu["m10"] / mu["m00"]), (mu["m01"] / mu["m00"])

            if x < 300:
                return "L"
            elif 300 <= x < 500:
                return "F"
            elif 500 <= x:
                return "R"

    def run(self):
        
        
        received_text = self.cc.check()
        cc_checkpoint = time.time()
        if received_text == 'run':
            wc = WheelControl()
            while (self.cap.isOpened()):

                # image processing -------------------
                # フレームを取得
                ret, frame = self.cap.read()
                
                command = self.face2command(frame)            
                """
                # 赤色検出
                mask = self.red_detect(frame)

                # 結果表示
                # cv2.imshow("Frame", frame)
                # cv2.imshow("Mask", mask)
                command = self.gravity_center(mask)
                """

                if command != None:
                    # print(command)
                    print("try")
                    if(command == "F"):
                        print(command)
                        wc.forward(duty=20)
                    elif(command == "B"):
                        print(command)
                        wc.backward(duty=20)
                    elif(command == "L"):
                        print(command)
                        wc.rotate_left(duty=10)
                    elif(command == "R"):
                        print(command)
                        wc.rotate_right(duty=10)
                    elif(command == "W"):
                        print(command)
                        wc.forward(duty=0)

                    print("done")

                # qキーが押されたら途中終了
                #if cv2.waitKey(25) & 0xFF == ord('q'):
                #   break
                
                # chack per 5sec for ngrok. 
                if time.time() - cc_checkpoint > self.dt_check:
                    cc_checkpoint = time.time()
                    received_text = self.cc.check()
                    if received_text == 'stop':
                        wc.forward(duty=0)
                        break
                    
                time.sleep(self.dt)
            self.cap.release()
        # cv2.destroyAllWindows()
        elif received_text == 'stop':
            None
        else:
            None
