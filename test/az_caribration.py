#!/usr/bin/env python

import time

from icm20948 import ICM20948

imu = ICM20948()
sum_az=0

for i in range(10):
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
    print(az)
    sum_az = sum_az+az
    time.sleep(0.25)

ave_az = sum_az/10
print("ave_az",str(ave_az))


