#coding:utf-8


import RPi.GPIO as GPIO
import time
import cv2
from motor_ctr import *
from nine_axis import *
from camera import *
from parachute import *

bgr = [10,10,130]
cap = cv2.VideoCapture(0)

def  main():

    #例えばwhileループとかで待ち作る？
    while release_detect()==0:
        print("False")
    #落下検知も放出検知と同様
    drop_detect()
    parachute_sep()
    angle = estimate_pos()
    turn(angle)
    func_forward()
    #画像取得

    while True:
        ret, img = cap.read()
        ThreshImage = img_thresh(img,bgr)
        object_centerX = calc_center(ThreshImage)[0]
        print("centerX : " + str(object_centerX))
        #画面中心のX座標
        screen_centerX = img.shape[1]/2

        #物体の重心座標の位置によって回転方向決める
        if object_centerX > screen_centerX:
            func_right()
        elif object_centerX < screen_centerX:
            func_left()
        else:
            func_forward()

        """
        終了条件を満たせばwhileループから抜け出す
        if ~~  終了条件
            break
        """

        while True:
            print("Goal!")

main()

