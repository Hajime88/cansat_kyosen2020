#!/usr/bin/env python

from icm20948 import ICM20948
import time
import math

print("""magnetometer.py - Convert raw values to heading

Rotate the sensor (X-axis upwards) through 360 degrees to calibrate.

Press Ctrl+C to exit!

""")

X = 0
Y = 1
Z = 2

# The two axes which relate to heading, depends on orientation of the sensor
# Think Left & Right, Forwards and Back, ignoring Up and Down
AXES = X, Y

#Initialise the imu
imu = ICM20948()

while True:
    # Read the current, uncalibrated, X, Y & Z magnetic values from the magnetometer and save as a list
    mag = list(imu.read_magnetometer_data())
    
    # Convert from Gauss values in the appropriate 2 axis to a heading in Radians using trig
    # Note this does not compensate for tilt
    heading = math.atan2(
            mag[AXES[0]],
            mag[AXES[1]])
    
    # Convert heading from Radians to Degrees
    heading = math.degrees(heading)
    # Round heading to nearest full degree
    heading = round(heading) 

    # Note: Headings will not be correct until a full 360 deg calibration turn has been completed to generate amin and amax data
    print("Heading: {}".format(heading))

    time.sleep(0.1)