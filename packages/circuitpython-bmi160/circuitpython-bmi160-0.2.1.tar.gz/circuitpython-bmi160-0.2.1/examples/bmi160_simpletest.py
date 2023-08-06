# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import bmi160 as BMI160


i2c = board.I2C()  # uses board.SCL and board.SDA
bmi = BMI160.BMI160(i2c)

while True:
    accx, accy, accz = bmi.acceleration
    print("Acceleration X: ", accx)
    print("Acceleration Y: ", accy)
    print("Acceleration Z: ", accz)
    gyrox, gyroy, gyroz = bmi.gyro
    print("Gyro X: ", gyrox)
    print("Gyro Y: ", gyroy)
    print("Gyro Z: ", gyroz)
    time.sleep(0.5)
