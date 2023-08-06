# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import mc3479 as MC3479


i2c = board.I2C()  # uses board.SCL and board.SDA
mc3479 = MC3479.MC3479(i2c)

while True:
    accx, accy, accz = mc3479.acceleration
    print("Acceleration X: ", accx)
    print("Acceleration Y: ", accy)
    print("Acceleration Z: ", accz)
    time.sleep(0.5)
