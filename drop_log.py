from parachute import *
import time
from icm20948 import ICM20948
from led import *
from serialsend import *
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
drop_counter2 = 0
impact_counter = 0
land_counter = 0
#green_light_on()



def drop_land_detect():

    #drop_counterは試験をして調整
    while drop_counter < 3:
        atotal = get_atotal()
        serial_write("not detect drop "+str(atotal))
        write_csv(atotal)

        if atotal < 0.2:
            serial_write("falling! "+str(atotal))
            write_csv(atotal)
            drop_counter = drop_counter + 1
        time.sleep(0.01)

    start_time = time.perf_counter()
    limit_time = 30

    while parachute_counter < 1:
        atotal = get_atotal()
        serial_write("not detect parachute "+str(atotal))
        write_csv(atotal)
        if abs(atotal) > 10:
            t = 0
            while t <10:
                serial_write("parachute opened! "+str(atotal))
                write_csv(atotal)
                #time.sleep(0.01)
                atotal = get_atotal()
                t = t + 1
            parachute_counter = parachute_counter + 1
        
        if time.perfcounter() -  start_time > limit_time:
            serial_write("time out! ")
            break
        
        time.sleep(0.01)

    while drop_counter2 < 3:
        atotal = get_atotal()
        serial_write("not detect drop "+str(atotal))
        write_csv(atotal)

        if atotal < 3:
            serial_write("dropping with parachute! "+str(atotal))
            write_csv(atotal)
            drop_counter2 = drop_counter2 + 1
        
        if time.perfcounter() -  start_time > limit_time:
            serial_write("time out! ")
            break
        
        time.sleep(0.01)


    while impact_counter < 1:
        atotal = get_atotal()
        serial_write("not detect impact "+str(atotal))
        write_csv(atotal)
        if abs(atotal) > 30:
            t = 0
            while t < 10:
                serial_write("impact! "+str(atotal))
                write_csv(atotal)
                #time.sleep(0.01)
                atotal = get_atotal()
                t = t + 1
            impact_counter = impact_counter + 1
        
        if time.perfcounter() -  start_time > limit_time:
            serial_write("time out! ")
            break;
        
        time.sleep(0.01)

    while land_counter < 200:
        atotal = get_atotal()
        serial_write("landed! "+str(atotal))
        write_csv(atotal)
        land_counter = land_counter + 1
        time.sleep(0.01)

    #green_light_off()
    #red_light_on()
    #parachute_sep()
    #red_light_off()


