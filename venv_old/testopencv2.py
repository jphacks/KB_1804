# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
##from wheel_control import WheelControl
##import RPi.GPIO as GPIO
import time

class OpticalSense:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.width = self.cap.get(3)
        self.height = self.cap.get(4)
        
    def face2command(self, img):
        cascade_path = "./haarcascade/haarcascade_frontalcatface.xml"
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(cascade_path)
        facerects = cascade.detectMultiScale(img_gray,
                                            scaleFactor=1.1,
                                            minNeighbors=1,
                                            minSize=(100, 100))
        
        x_center = self.width / 2
        print(facerects)
        if facerects != ():
            
            x, y = facerects[0][0], facerects[0][1]
            w, h = facerects[0][2], facerects[0][3]
            
            face_center = x + w//2
            width_ex = 100

            area_img = self.width * self.height

            if face_center < x_center - width_ex:
                command = "Left"
            elif face_center > x_center + width_ex:
                command = "Right"
            elif w * h > area_img * 0.5:
                command = "Backward"
            elif w * h < area_img * 0.3:
                command = "Forward"
            else:
                command =" Wait"
        else:
            command = "Wait"
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
        ##wc = WheelControl()
        while (self.cap.isOpened()):
            # フレームを取得
            ret, frame = self.cap.read()
            
            command_ = self.face2command(frame) #############
            
            
            # 赤色検出
            mask = self.red_detect(frame)

            # 結果表示
            cv2.imshow("Frame", frame)
            cv2.imshow("Mask", mask)
            command = self.gravity_center(mask)
            

            if command != None:
                print(command)
                try:
                    
                    if(command == "Foward"):
                        ##wc.forward(duty=100)
                        print("Foward")
                        time.sleep(1)
                    elif(command == "Back"):
                        ##wc.backward(duty=100)
                        print("Back")
                        time.sleep(1)
                    elif(command == "Left"):
                        ##wc.rotate_left(duty=50)
                        print("Left")
                        time.sleep(1)
                    elif(command == "Right"):
                        ##wc.rotate_right(duty=50)
                        print("Right")
                        time.sleep(1)
                    elif(command == "Wait"):
                        print("Wait")
                        ##wc.stop()

                    print("done")

                except:
                    print("except")
                    ##GPIO.cleanup()

                finally:
                    print("fin")
                    ##GPIO.cleanup()

                # qキーが押されたら途中終了
            #if cv2.waitKey(25) & 0xFF == ord('q'):
            #   break

        self.cap.release()
        # cv2.destroyAllWindows()

