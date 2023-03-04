#coding:utf-8

import RPi.GPIO as GPIO
import time
import cv2
#from nine_axis import *
from camera import *
from parachute import *
from motor_final import *
import math
from judge_movement import *
from drop_log import *
from serialsend import *

#クレーンとゴールの距離:要計測
CraneToGoal = 30  #クレーンからゴールまでの距離
direction = 90 #クレーンからゴールへの方向
bgr = [10,10,130]

not_detect_counter = 0
#クレーンから半径20mの領域に落ちると仮定
R_search = 20

def  main():
    ser = None
    serial_open()

    #落下検知
    drop_land_detect()

    #ニクロム線焼き切り
    parachute_sep()
    #パラシュートから離れる
    forward(1)
    serial_write("left from parachute..")

    #キャリブレーション
    serial_write("calibration start!")
    nine_axis_calib()
    serial_write("caliblation finished!")

    #クレーンからゴールへの方向directionに向かってCraneToGoalだけ進む
    n = 5 #直進距離をn分割して方向を修正しながら進む
    for i in range(n):
        serial_write("moving to virtual goal.. [i+1]")
        adjust(direction) 
        forward(CraneToGoal/n)

######################################
    # #この条件式は要検討,直進部分
    # while not_detect_counter < 10:
    #     not_detect_counter = capture_judge(bgr,not_detect_counter)
    
    # rotation(135)

    # #直進で調べ切れていない部分を四角形に動いて調べる
    # for i in range(4):
    #     for j in range(3):
    #         forward(R_search*math.sqrt(2)/3)
    #         capture_judge(bgr)
    #     rotation(90)

    # while True:
    #     serial_write("I could not detect redcorn, stop!!")

    forward(10) #最初の探索円の中心

    capture_judge()
    rotation(-45)
    forward(10*math.sqrt(2))

    capture_judge()
    rotation(90)
    forward(10*math.sqrt(2))

    capture_judge()
    rotation(90)
    forward(10*math.sqrt(2))

    capture_judge()

##ここからどうしましょう



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()