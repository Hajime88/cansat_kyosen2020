from nine_axis import *
from parachute import *
import time
from icm20948 import ICM20948



imu = ICM20948()
vx, vy, vz = 0, 0, 0
x, y, z = 0, 0, 0
thetax, thetay, thetaz = 0, 0, 0
filterCoefficient = 0.9
lowpass_ax, lowpass_ay, lowpass_az = 0, 0, 0
highpass_ax, highpass_ay, highpass_az = 0, 0, 0
timespan =0.25
old_ax, old_ay, old_az, old_vx, old_vy, old_vz = 0, 0, 0, 0, 0, 0


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
stop_counter = 0

#drop_counterは試験をして調整
while drop_counter < 10:
    atotal = get_atotal()
    print("not detect drop",atotal)
    if atotal < 0.4:
        print("falling!",atotal)
        drop_counter = drop_counter + 1
    time.sleep(0.01)
    

while stop_counter < 1:
    atotal = get_atotal()
    print("not detect stop",atotal)
    if abs(atotal) > 10:
        print("impact!",atotal)
        stop_counter = stop_counter + 1
    time.sleep(0.01)

print("landed!")

parachute_sep()
