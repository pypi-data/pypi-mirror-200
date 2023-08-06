# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import board
import mc3479 as MC3479


i2c = board.I2C()  # uses board.SCL and board.SDA
mc3479 = MC3479.MC3479(i2c)
