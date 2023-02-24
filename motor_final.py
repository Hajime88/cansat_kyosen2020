#モーター

#ライブラリのインポート
import RPi.GPIO as GPIO
import time
import math

#encoder_finalのインポート→よく分からんから任せた！
from encoder_final import distance, pulse_count, enc_destroy

AIN1 = 16
AIN2 = 18 
PWMA = 12
BIN1 = 36
BIN2 = 38
PWMB = 35

#ここから初期設定#

GPIO.setmode(GPIO.BOARD) #エンコーダ側とBOARD,BCMはそろえた方がよい？

#各ピンを出力に設定
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
#ここまで#

#ブレーキの関数
def brake():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.HIGH)

    time.sleep(3)  #3秒間は停止

#前進の関数
#d[m]進むまで前進
def forward(d):
    l = 0 #[m]これが進んだ距離

    #モーターを正方向に回転
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)

    while(l < d):
        #エンコーダで距離を計測(約1秒ごとに値を取得)
        R_d, L_d = distance() #エンコーダのファイルより
        l = l+(R_d+L_d)/2

#後退の関数
#d[m]戻るまで後退
def back(d):
    l = 0 #これが後退した距離

    #モーターを逆方向に回転
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)

    while(l<d):
        #エンコーダで距離を計測
        R_d, L_d = -distance() #エンコーダのファイルより
        l = l+(R_d+L_d)/2

#回転の関数
#進行方向に対して左にi[deg]だけ回転(-180<i<180)
def rotation(i):
    fai = 0 #[deg] ここに回転角を入力
    W = 0.15 #[m] タイヤ間距離

    if i > 0:
        #右輪は前進、左輪は後退(中心位置は固定)
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)
    
    else:
        #右輪は後退、左輪は前進
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        GPIO.output(BIN1, GPIO.HIGH)
        GPIO.output(BIN2, GPIO.LOW)

    while(abs(fai) < abs(i)):
        R_d, L_d = distance() #エンコーダのファイルより
        fai = fai+(R_d-L_d)/W*180/math.pi

#終了用
def destroy():
    #PWM信号の停止
    p_a.stop()
    p_b.stop()

    #GPIOピンの解放
    GPIO.cleanup()

    #エンコーダに関するピンも解放
    enc_destroy()

    print("end of program")

#試験用のプログラム
def test(forward, back, turn):
    forward(forward)
    brake()

    back(back)
    brake()

    rotation(turn)
    brake()

    destroy()
