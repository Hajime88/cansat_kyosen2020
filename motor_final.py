#モーター+九軸センサー

#ライブラリのインポート
import RPi.GPIO as GPIO
import time
import math

from icm20948 import ICM20948
from parachute import *
from led import *
from serialsend import *
import serial
import datetime
import csv
import os

AIN1 = 23 
AIN2 = 24  
PWMA = 18 
BIN1 = 20 
BIN2 = 16 
PWMB = 19 

LXPin = 7
LAPin = 12
LBPin = 1
RXPin = 4
RAPin = 27 
RBPin = 17

#ここから初期設定#
GPIO.setmode(GPIO.BCM) 

#各ピンの入出力に設定
GPIO.setup(AIN1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(AIN2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(PWMA, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(BIN1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(BIN2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(PWMB, GPIO.OUT, initial = GPIO.LOW)

GPIO.setup(LXPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LAPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LBPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(RXPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(RAPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(RBPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

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
##ここまで

##ここからエンコーダの関数の定義
#エンコーダのパルスをカウント
def pulse_count(APin, BPin):
    count = 0
    start = time.perf_counter()
    
    while (time.perf_counter()-start < 0.05):
        a = GPIO.wait_for_edge(APin, GPIO.FALLING, timeout=50)
      
        if a is None:
            count = 0
        else:
            if GPIO.input(BPin) == 1:
                count = count-1
            else:
                count = count+1
    return(count)

#タイヤがそれぞれ進んだ距離の算出(今は0.2秒ごと)
def distance():
    pulse = 500 #ppr
    l = 2*0.055*math.pi #[m] タイヤが一回転する間に進む距離
    k = 0.9 #値を調整するための係数:要調整
    
    R_count_1 = pulse_count(RAPin, RBPin)
    L_count_1 = pulse_count(LAPin, LBPin)
    L_count_2 = pulse_count(LAPin, LBPin)
    R_count_2 = pulse_count(RAPin, RBPin)
        
    R_count = -(R_count_1+R_count_2)*2
    L_count = (L_count_1+L_count_2)*2

    R_d = l*R_count/pulse/k #[m]
    L_d = l*L_count/pulse/k #[m]

    return R_d, L_d
##ここまでエンコーダ

##ここから九軸センサの関数定義
serial_write("""magnetometer.py - Convert raw values to heading
Rotate the sensor (Z-axis downwards) through 360 degrees to calibrate.
""")

X = 0
Y = 1
Z = 2

# The two axes which relate to heading, depends on orientation of the sensor
# Think Left & Right, Forwards and Back, ignoring Up and Down
AXES = Y, X

# Initialise the imu
imu = ICM20948()

# Store an initial two readings from the Magnetometer
amin = list(imu.read_magnetometer_data())
amax = list(imu.read_magnetometer_data())

#def get_az():
#    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
#    az = az-0.997
#    serial_write(az)
def nine_axis_calib():
    global amin, amax

    #デューティを設定(0~100の範囲で指定)
    val_calib = 80

    #デューティ比を設定
    p_a.ChangeDutyCycle(val_calib)
    p_b.ChangeDutyCycle(val_calib)

    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)

    start_time = time.perf_counter()

    while(time.perf_counter() - start_time < 6):
        # Read the current, uncalibrated, X, Y & Z magnetic values from the magnetometer and save as a list
        mag = list(imu.read_magnetometer_data())
        
        ## Step through each uncalibrated X, Y & Z magnetic value and calibrate them the best we can ##
        for i in range(3):
            v = mag[i]
            # If our current reading (mag) is less than our stored minimum reading (amin), then save a new minimum reading
            # ie save a new lowest possible value for our calibration of this axis
            if v < amin[i]:
                amin[i] = v
            # If our current reading (mag) is greater than our stored maximum reading (amax), then save a new maximum reading
            # ie save a new highest possible value for our calibration of this axis
            if v > amax[i]:
                amax[i] = v
            
            # Calibrate value by removing any offset when compared to the lowest reading seen for this axes
            mag[i] -= (amin[i]+amax[i])/2
            
            # Scale value based on the higest range of values seen for this axes
            # Creates a calibrated value between 0 and 1 representing magnetic value
            try:
                mag[i] /= (amax[i] - amin[i])/2
            except ZeroDivisionError:
                pass
    #         # Shift magnetic values to between -0.5 and 0.5 to enable the trig to work
    #        mag[i] += 0.5

        # Convert from Gauss values in the appropriate 2 axis to a heading in Radians using trig
        # Note this does not compensate for tilt
        heading = math.atan2(
                mag[AXES[0]],
                mag[AXES[1]])

        # If heading is negative, convert to positive, 2 x pi is a full circle in Radians
    #     if heading < 0:
    #         heading += 2 * math.pi
            
        # Convert heading from Radians to Degrees
        heading = math.degrees(heading)
        # Round heading to nearest full degree
        heading = round(heading) 

        ##########
        ## Note:## Headings will not be correct until a full 360 deg calibration turn has been completed to generate amin and amax data ##
        ##########
        
        serial_write("Heading: {}".format(heading))
        #serial_write(mag)

    
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)

    serial_write("calibrated!!")
    time.sleep(3)
    return amin, amax

def get_heading():

    mag = list(imu.read_magnetometer_data())
    for i in range(3):
        mag[i] -= (amin[i] + amax[i])/2
        mag[i] /= (amax[i] - amin[i])/2
    # Convert from Gauss values in the appropriate 2 axis to a heading in Radians using trig
    # Note this does not compensate for tilt
    heading = math.atan2(
            mag[AXES[0]],
            mag[AXES[1]])

    # If heading is negative, convert to positive, 2 x pi is a full circle in Radians
    #     if heading < 0:
    #         heading += 2 * math.pi
            
    # Convert heading from Radians to Degrees
    heading = math.degrees(heading)
    # Round heading to nearest full degree
    heading = round(heading) 

    ##########
    ## Note:## Headings will not be correct until a full 360 deg calibration turn has been completed to generate amin and amax data ##
    ##########
    
    serial_write("Heading: {}".format(heading))
    #serial_write(mag)
    
    #time.sleep(0.1)
    
    return heading
##ここまで九軸の定義

##ここからモーターの関数定義
#ブレーキの関数
def brake():
    #デューティを設定(0~100の範囲で指定)
    val_brake = 50

    #デューティ比を設定
    p_a.ChangeDutyCycle(val_brake)
    p_b.ChangeDutyCycle(val_brake)

    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.HIGH)

    time.sleep(1)  #1秒間は停止

#前進の関数
#d[m]進むまで前進
def forward(d):
    l = 0 #[m]これが進んだ距離

    #デューティを設定(0~100の範囲で指定)
    val_forward = 100

    #デューティ比を設定
    p_a.ChangeDutyCycle(val_forward)
    p_b.ChangeDutyCycle(val_forward)

    t_start = time.perf_counter()

    #モーターを正方向に回転
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)

    while(l < d):
        #エンコーダで距離を計測(約1秒ごとに値を取得)
        R_d, L_d = distance() #エンコーダのファイルより
        l = l+(R_d+L_d)/2
        serial_write(l) #練習用

        #エンコーダで値が取れなくなったときの回避
        if time.perf_counter() - t_start > d*6: #要確認
            serial_write("Attention! Encoder has no value!")
            break;
    
    
    brake()

#後退の関数
#d[m]戻るまで後退
def back(d):
    l = 0 #これが後退した距離

    #デューティを設定(0~100の範囲で指定)
    val_back = 80

    #デューティ比を設定
    p_a.ChangeDutyCycle(val_back)
    p_b.ChangeDutyCycle(val_back)

    t_start = time.perf_counter()

    #モーターを逆方向に回転
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)

    while(l<d):
        #エンコーダで距離を計測
        R_d, L_d = distance() #エンコーダのファイルより
        l = l-(R_d+L_d)/2
        serial_write(-l) #練習用

        #エンコーダで値が取れなくなったとき用
        if time.perf_counter() - t_start > d*8: #要確認
            serial_write("Attention! Encoder has no value!")
            break;
    
    
    brake()

#回転の関数
#進行方向に対して左にi[deg]だけ回転(-180<i<180)
def rotation(i):
    #デューティを設定(0~100の範囲で指定)
    val_rot = 50

    #デューティ比を設定
    p_a.ChangeDutyCycle(val_rot)
    p_b.ChangeDutyCycle(val_rot)

    fai = get_heading() #九軸から現在の方向を取得
    theta = fai+i #目標角度 取得

    #thetaを-180~180に修正
    if theta < -180:
        theta = theta+360
    elif 180 < theta:
        theta = theta-360

    if i > 0:
        #右輪は前進、左輪は停止
        GPIO.output(AIN1, GPIO.HIGH)
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
        GPIO.output(BIN1, GPIO.HIGH)
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
    
    brake()
        
        
            
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

    serial_write("end of program")
    

#試験用のプログラム
def test(x, y, turn):
    forward(x)

    back(y)

    rotation(turn)

    destroy()
##ここまでがモーターの関数定義

#if __name__ == '__main__':
    #try:
    #   serial_open()
    #   nine_axis_calib()
    #   serial_write("trying")
    #   get_heading()  
    #    test(0.7, 0, 90)
    #except KeyboardInterrupt:
    #    destroy()
    #    serial_write("trying")