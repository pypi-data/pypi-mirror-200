# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import board
import mc3479 as MC3479


i2c = board.I2C()  # uses board.SCL and board.SDA
mc3479 = MC3479.MC3479(i2c)

print("Current Acceleration Range")
print("Acceleration Range", mc3479.acceleration_range)
print("Changing Acceleration range to 8G")
mc3479.acceleration_range = MC3479.ACCEL_RANGE_8G
print("Acceleration Range", mc3479.acceleration_range)
print("Changing Acceleration Range to 4G")
mc3479.acceleration_range = MC3479.ACCEL_RANGE_4G
print("Acceleration Range", mc3479.acceleration_range)
print("Changing Acceleration Range to 16G")
mc3479.acceleration_range = MC3479.ACCEL_RANGE_16G
print("Acceleration Range", mc3479.acceleration_range)
