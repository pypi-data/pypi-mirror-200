# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import board
import mc3479 as MC3479


i2c = board.I2C()  # uses board.SCL and board.SDA
mc3479 = MC3479.MC3479(i2c)

print("Current Acceleration data rate", mc3479.acceleration_output_data_rate)
print("Changing Acceleration data rate to 25 Hz")
mc3479.acceleration_output_data_rate = MC3479.BANDWIDTH_25
print("Changed Acceleration data rate", mc3479.acceleration_output_data_rate)
print("Changing Acceleration data rate to 62.5 Hz")
mc3479.acceleration_output_data_rate = MC3479.BANDWIDTH_62_5
print("Changed Acceleration data rate", mc3479.acceleration_output_data_rate)
print("Changing Acceleration data rate to 1000")
mc3479.acceleration_output_data_rate = MC3479.BANDWIDTH_1000
print("Changed Acceleration data rate", mc3479.acceleration_output_data_rate)
