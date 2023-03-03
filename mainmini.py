#coding:utf-8

#import RPi.GPIO as GPIO
import time
import cv2
#from nine_axis import *
from camera import *
#from parachute import *
from motor_final import *
from judge_movement import *

cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
#cap.set(cv2.CAP_PROP_EXPOSURE,1000)
not_detect_counter = 0

def  main():
    global not_detect_counter
    not_detect_counter = capture_judge(cap,not_detect_counter)
    """
    ret, img = cap.read()
    #画像の上下左右反転
    RevImg = cv2.flip(img,-1)
    cv2.imwrite("image.jpg",RevImg)
    ThreshImage = img_thresh(RevImg)
    cv2.imwrite("BWimage.jpg",ThreshImage)
    object_centerX = calc_center(ThreshImage,not_detect_counter)[0]
    print("centerX : " + str(object_centerX))
    #画面中心のX座標
    screen_centerX = RevImg.shape[1]/2
    print("screen_centerX: " + str(screen_centerX))
    center_diff = object_centerX - screen_centerX
    #print("center_diff:"+str(center_diff))
    if center_diff > 100:
        print("turn right!!")
        rotation(-10)
        brake()
    elif center_diff < -100:
        print("turn left!!")
        rotation(10)
        brake()
    else :
        print("forward!!")
        forward(0.1)
        brake()
    """
    #終了条件を満たせばwhileループから抜け出す
    #if ~~  終了条件
     #   break
    """
    """

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()
