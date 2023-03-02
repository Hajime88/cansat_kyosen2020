#!/usr/bin/env python

import time
from icm20948 import ICM20948
from motor_final import *
from encoder_final import *


imu = ICM20948()

print("""magnetometer.py - Convert raw values to heading

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
#    print(az)
def nine_axis_calib():
    fai = 0
    W = 0.2
    global amin, amax
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)

    while(1000 < abs(fai)):
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
        
        print("Heading: {}".format(heading))
        #print(mag)

        R_d, L_d =distance()
        fai = fai+(R_d-L_d)/W*180/math.pi
    
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)
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
    
    print("Heading: {}".format(heading))
    #print(mag)
    return heading

"""
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

    while True:
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
"""

if __name__ == '__main__':
    nine_axis_calib()
    while True:
        get_heading()
