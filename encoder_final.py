# encoder final.ver

import RPi.GPIO as GPIO
import math
import time

LXPin = 7 #26 (BOARD)
LAPin = 12 #32
LBPin = 1  #28
RXPin = 4 #7
RAPin = 27 #13
RBPin = 22 #15

#初期設定
GPIO.setmode(GPIO.BCM) #BOARDにそろえた方がよい？
GPIO.setup(LXPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LAPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LBPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(RXPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(RAPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(RBPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#エンコーダのパルスをカウント
def pulse_count(APin, BPin):
    count = 0
    start = time.perf_counter()
    
    while (time.perf_counter()-start < 0.25):
        a = GPIO.wait_for_edge(APin, GPIO.FALLING, timeout=250)
      
        if a is None:
            count = 0
        else:
            if GPIO.input(BPin) == 1:
                count = count-1
            else:
                count = count+1
    return(count)

#タイヤがそれぞれ進んだ距離の算出(今は1秒ごと)
def distance():
    pulse = 500 #ppr
    l = 0.4 #[m] タイヤが一回転する間に進む距離:要再計測
    k = 1 #値を調整するための係数:要調整
    
    R_count_1 = pulse_count(RAPin, RBPin)
    L_count_1 = pulse_count(LAPin, LBPin)
    L_count_2 = pulse_count(LAPin, LBPin)
    R_count_2 = pulse_count(RAPin, RBPin)
        
    R_count = -(R_count_1+R_count_2)*2
    L_count = (L_count_1+L_count_2)*2

    R_d = l*R_count/pulse/k #[m]
    L_d = l*L_count/pulse/k #[m]

    return R_d, L_d

#位置の推定
def location(x, y, fai, R_d, L_d):
    W = 0.15 #[m] タイヤ間距離

    fai = fai+(R_d-L_d)/W #[rad]
    x = x+(R_d+L_d)/2*math.cos(fai/2) #[m]
    y = y+(R_d+L_d)/2*math.sin(fai/2) #[m]
    
    return x, y, fai

#終了する用
def enc_destroy():
    GPIO.cleanup()
    print("program end")


def loop():
    x = 0
    y = 0
    fai = 0
    
    while True:
        R_d, L_d = distance()
        
        x, y, fai = location(x, y, fai, R_d, L_d)
        print(x, y)

#1秒ずつ位置を出力
if __name__ == '__main__':
    loop()
