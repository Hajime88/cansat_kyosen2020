#!/usr/bin/env python

import time

from icm20948 import ICM20948


imu = ICM20948()

def get_az():
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
    az = az-0.997
    #print(az)
    