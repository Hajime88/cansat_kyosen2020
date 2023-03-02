#モーター

#ライブラリのインポート
import RPi.GPIO as GPIO
import time
import math
from nine_axis import get_heading

#encoder_finalのインポート
from encoder_final import distance, pulse_count

AIN1 = 23 #16(BOARD)
AIN2 = 24 #18 
PWMA = 18 #12
BIN1 = 20 #38
BIN2 = 16 #36
PWMB = 19 #35 ここは前進、後退を要確認

#ここから初期設定#

GPIO.setmode(GPIO.BCM) 

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
        print(l) #練習用

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
        R_d, L_d = distance() #エンコーダのファイルより
        l = l-(R_d+L_d)/2
        print(l) #練習用

#回転の関数
#進行方向に対して左にi[deg]だけ回転(-180<i<180)
def rotation(i):
    fai = get_heading() #九軸から現在の方向を取得
    W = 0.2 #[m] タイヤ間距離
    theta = fai+i #目標角度 取

    #thetaを-180~180に修正
    if theta < -180:
        theta = theta+360
    elif 180 < theta:
        theta = theta-360

    if i > 0:
        #右輪は前進、左輪は停止
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.LOW)
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)
        
        #180前後の不連続点を回避
        if theta < -160:
            theta = theta + 360
            
            if fai < -160:
                fai = fai + 360

        if theta < fai :
            theta = theta + 360
            while(fai < theta):
                read_angle = get_heading()
                if read_angle < 0:
                    fai = fai + 360
                else:
                    fai = read_angle

        else:
            while(fai < theta):
                fai = get_heading()
                if fai < -160:
                    fai = fai + 360

    else:
        #右輪は停止、左輪は前進
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.LOW)

        if theta > 160:
            theta = theta - 360
            
            if fai > 160:
                fai = fai - 360

        if theta > fai :
            theta = theta - 360
            while(fai > theta):
                read_angle = get_heading()
                if read_angle > 0:
                    fai = fai - 360
                else:
                    fai = read_angle

        else:
            while(fai > theta):
                fai = get_heading()
                if fai > 160:
                    fai = fai - 360
        
        
            
# 方位を入力しての角度調整
def adjust(direction):
    fai = get_heading() #現在の方向

    i = direction - fai #向きたい方向との角度差

    #iを-180~180に調整
    if i < -180:
        i = i + 360
    elif 180 < i:
        i = i - 360
    
    #角度iだけ回転させる
    rotation(i)

#終了用
def destroy():
    #PWM信号の停止
    p_a.stop()
    p_b.stop()

    #ピンを停止状態に戻す
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)

    #GPIOピンの解放
    GPIO.cleanup()

    print("end of program")

#試験用のプログラム
def test(x, y, turn):
    forward(x)
    brake()

    back(y)
    brake()

    rotation(turn)
    brake()

    destroy()
    
try:
    print("trying")
#    test(0, 0, 45)
except KeyboardInterrupt:
    destroy()
    print("program stopped")
