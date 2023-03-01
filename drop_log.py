from nine_axis import *
from parachute import *
import time
from icm20948 import ICM20948
from led import *
import serial
import datetime
import csv
import os


imu = ICM20948()
vx, vy, vz = 0, 0, 0
x, y, z = 0, 0, 0
thetax, thetay, thetaz = 0, 0, 0
filterCoefficient = 0.9
lowpass_ax, lowpass_ay, lowpass_az = 0, 0, 0
highpass_ax, highpass_ay, highpass_az = 0, 0, 0
timespan =0.25
old_ax, old_ay, old_az, old_vx, old_vy, old_vz = 0, 0, 0, 0, 0, 0

#if(os.path.isfile('drop_accel_data.csv')):
#    os.remove('drop_accel_data.csv')
#f = open('drop_accel_data.csv', 'w')
#f.close()
def write_csv(data):
    dt_now = datetime.datetime.now()
    with open('drop_accel_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([dt_now, data])

def get_atotal():
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()

    ## filter ##
    #ax, ay, az = ax, ay-0.03, az-1.01  #case of nineaxesA
    #ax, ay, az = ax-0.01, ay+0.025, az-1.01  #case of nineaxesB

    ## calculate total accel ##
    atotal = ax**2 + ay**2 +az**2

    #print("Accel_Total: {:05.4f} ".format(atotal))
    return atotal

drop_counter = 0
parachute_counter = 0
impact_counter = 0
land_counter = 0
green_light_on()

def SerWrite(msg):
    ser.write((msg+"\r\n").encode("utf-8"))

try:
    ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.1)
    print("open serial port")
    SerWrite("open serial port")
except:
    print("cannot open serial port")
    exit(1)   

#drop_counterは試験をして調整
while drop_counter < 5:
    atotal = get_atotal()
    print("not detect drop",atotal)
    SerWrite("not detect drop "+str(atotal))
    write_csv(atotal)

    if atotal < 0.1:
        print("falling!",atotal)
        SerWrite("falling! "+str(atotal))
        write_csv(atotal)
        drop_counter = drop_counter + 1
    time.sleep(0.01)


while parachute_counter < 1:
    atotal = get_atotal()
    print("not detect parachute",atotal)
    SerWrite("not detect parachute "+str(atotal))
    write_csv(atotal)
    if abs(atotal) > 30:
        t = 0
        while t <100:
            print("parachute opened!",atotal)
            SerWrite("parachute opened! "+str(atotal))
            write_csv(atotal)
            #time.sleep(0.01)
            atotal = get_atotal()
            t = t + 1
        parachute_counter = parachute_counter + 1
    
    time.sleep(0.01)

while impact_counter < 1:
    atotal = get_atotal()
    print("not detect impact",atotal)
    SerWrite("not detect impact "+str(atotal))
    write_csv(atotal)
    if abs(atotal) > 50:
        t = 0
        while t < 100:
            print("impact!",atotal)
            SerWrite("impact! "+str(atotal))
            write_csv(atotal)
            #time.sleep(0.01)
            atotal = get_atotal()
            t = t + 1
        impact_counter = impact_counter + 1
        time.sleep(0.01)

while land_counter < 500:
    atotal = get_atotal()
    print("landed!",atotal)
    SerWrite("landed! "+str(atotal))
    write_csv(atotal)
    land_counter = land_counter + 1
    time.sleep(0.01)

green_light_off()
red_light_on()
#parachute_sep()
time.sleep(10)
red_light_off()
