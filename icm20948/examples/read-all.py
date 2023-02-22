#!/usr/bin/env python

import time

from icm20948 import ICM20948

print("""read-all.py

Reads all ranges of movement: accelerometer, gyroscope and

compass heading.

Press Ctrl+C to exit!

""")

imu = ICM20948()
vx, vy, vz = 0, 0, 0
x, y, z = 0, 0, 0
thetax, thetay, thetaz = 0, 0, 0
filterCoefficient = 0.9
lowpass_ax, lowpass_ay, lowpass_az = 0, 0, 0
highpass_ax, highpass_ay, highpass_az = 0, 0, 0
timespan =0.25
old_ax, old_ay, old_az, old_vx, old_vy, old_vz = 0, 0, 0, 0, 0, 0

while True:
    mx, my, mz = imu.read_magnetometer_data()
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
    # filter
    ax, ay, az = ax, ay-0.03, az-1.01
    # mx, my, mz = mx-11.5, my-6.5, mz+90
    # caluculate difference
    ax, ay, az = ax*9.792, ay*9.792, az*9.792
    lowpass_ax = lowpass_ax * filterCoefficient + ax * (1-filterCoefficient)
    lowpass_ay = lowpass_ay * filterCoefficient + ay * (1-filterCoefficient)
    lowpass_az = lowpass_az * filterCoefficient + az * (1-filterCoefficient)
    highpass_ax = ax - lowpass_ax
    highpass_ay = ay - lowpass_ay
    highpass_az = az - lowpass_az
    vx = ((highpass_ax + old_ax)*timespan) / 2 + vx
    old_ax = highpass_ax
    vy = ((highpass_ay + old_ay)*timespan) / 2 + vy
    old_ay = highpass_ay
    vz = ((highpass_az + old_az)*timespan) / 2 + vz
    old_az = highpass_az
    x = ((vx + old_vx)*timespan) / 2 + x
    old_vx = vx
    y = ((vy + old_vy)*timespan) / 2 + y
    old_vy = vy
    z = ((vz + old_vz)*timespan) / 2 + z
    old_vz = vz

    print("""
Accel: {:05.4f} {:05.4f} {:05.4f} m/s^2
Gyro:  {:05.2f} {:05.2f} {:05.2f}
Mag:   {:05.2f} {:05.2f} {:05.2f}
diff:  {:05.2f}m {:05.2f}m {:05.2f}m""".format(
        ax, ay, az, gx, gy, gz, mx, my, mz, x, y, z
        ))

    time.sleep(0.25)
