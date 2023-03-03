#coding:utf-8

import RPi.GPIO as GPIO
import time
import cv2
from nine_axis import *
from camera import *
from parachute import *
from motor_final import *
import math
from judge_movement import *


#クレーンとゴールの距離:要計測
CraneToGoal = 30
bgr = [10,10,130]

drop_counter = 0
stop_counter = 0
#クレーンから半径20mの領域に落ちると仮定
R_search = 20

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
    #パラシュートから離れる
    forward(1)

    #angle = get_heading()
    rotation(angle)
    forward(CraneToGoal)

    #この条件式は要検討,直進部分
    while not_detect_counter < 10:
        capture_judge(bgr)
    
    rotation(135)

    #直進で調べ切れていない部分を四角形に動いて調べる
    for i in range(4):
        for j in range(3):
            forward(R_search*math.sqrt(2)/3)
            capture_judge(bgr)
        rotation(90)

    while True:
        print("I could not detect redcorn, stop!!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()

