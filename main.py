#coding:utf-8

import RPi.GPIO as GPIO
import time
import cv2
from nine_axis import *
from camera import *
from parachute import *

bgr = [10,10,130]
drop_counter = 0
stop_counter = 0

cap = cv2.VideoCapture(0)

def  main():
    
    #落下検知
    while drop_counter < 1:
        az = get_az()
        print("not detect drop")
        if az > 1:
            drop_counter = drop_counter + 1

    #落下後停止検知
    while stop_counter < 12:
        az = get_az()
        print("not detect stop")
        if abs(az) < 0.01:
            stop_counter = stop_counter + 1

    #ニクロム線焼き切り
    parachute_sep()

    angle = estimate_pos()
    turn(angle)
    func_forward()
    #画像取得

    while True:
        ret, img = cap.read()
        #画像の上下左右反転
        RevImg = cv2.flip(img,-1)
        ThreshImage = img_thresh(RevImg,bgr)
        object_centerX = calc_center(ThreshImage)[0]
        print("centerX : " + str(object_centerX))
        #画面中心のX座標
        screen_centerX = RevImg.shape[1]/2

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

