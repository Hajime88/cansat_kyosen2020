#coding:utf-8


import RPi.GPIO as GPIO
import time


#ピン番号の割り当て方式を「コネクタのピン番号」に設定
GPIO.setmode(GPIO.BOARD)

#使用するピン番号を代入
AIN1 = 18
AIN2 = 16
PWMA = 12

BIN1 = 36
BIN2 = 38
PWMB = 35

#各ピンを出力ピンに設定
GPIO.setup(AIN1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(AIN2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(PWMA, GPIO.OUT, initial = GPIO.LOW)

GPIO.setup(BIN1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(BIN2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(PWMB, GPIO.OUT, initial = GPIO.LOW)

#PWMオブジェクトのインスタンスを作成
#出力ピン：12,35  周波数：100Hz
p_a = GPIO.PWM(PWMA,100)
p_b = GPIO.PWM(PWMB,100)

#PWM信号を出力
p_a.start(0)
p_b.start(0)

#デューティを設定(0~100の範囲で指定)
#速度は80%で走行する。
val = 80

#デューティ比を設定
p_a.ChangeDutyCycle(val)
p_b.ChangeDutyCycle(val)

#ブレーキする関数
def func_brake():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.HIGH)


#前進する関数
def func_forward():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)


#後進する関数
def func_back():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)


#右回転する関数
def func_right():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)


#左回転する関数
def func_left():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)

    
bgr = [10,10,130]

#放出検知
def release_detect():

#落下検知
def drop_detect():

#パラシュート分離
def sep_parachute():

#位置推定
def estimate_pos():
    angle = 0
    return angle

##モーター##
def turn_right(angle):

def turn_left(angle):

def turn(angle):
    if angle <= 0:
        turn_right(abs(angle))
    if angle >0:
        turn_left(angle)

def go_straight():

def img_thresh(img,bgr):

def calc_center(ThreshImage):

def  main():

    #例えばwhileループとかで待ち作る？
    while release_detect()==0:
        print("False")
    #落下検知も放出検知と同様
    drop_detect()
    sep_parachute()
    angle = estimate_pos()
    turn(angle)
    go_straight()
    #画像取得

while True:

    #photo_read()はラズパイのカメラから画像を読み込む関数
    img = photo_read()
    ThreshImage = img_thresh(img,bgr)
    object_centerX = calc_center(ThreshImage)[0]
    #画面中心のX座標
    screen_centerX = img.shape[1]/2

    #物体の重心座標の位置によって回転方向決める
    if object_centerX > screen_centerX:
        turn_right()
    elif object_centerX < screen_centerX:
        turn_left()
    else:
        go_straight()

    """
    終了条件を満たせばwhileループから抜け出す
    if ~~  終了条件
        break
    """

    while True:
        print("Goal!")

main()

