# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`mc3479`
================================================================================

MC3479 Accelerometer Driver


* Author(s): Jose D. Montoya

Implementation Notes
--------------------


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register

"""


from micropython import const
from adafruit_bus_device import i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct

try:
    from busio import I2C
    from typing_extensions import NoReturn
except ImportError:
    pass

__version__ = "0.0.1"
__repo__ = "https://github.com/jposada202020/CircuitPython_MC3479.git"

_I2C_ADDR = const(0x4C)
_REG_WHOAMI = const(0x98)

# pylint: disable= invalid-name, too-many-instance-attributes, missing-function-docstring
# pylint: disable=too-few-public-methods


class MC3479:
    """Driver for the MC3479 Sensor connected over I2C.

    :param ~busio.I2C i2c_bus: The I2C bus the MC3479 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x4C`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`MC3479` class.
    First you will need to import the libraries to use the sensor

        .. code-block:: python

            import board
            import mc3479 as MC3479

    Once this is done you can define your `board.I2C` object and define your sensor object

        .. code-block:: python

            i2c = board.I2C()  # uses board.SCL and board.SDA
            mc3479 = MC3479.MC3479(i2c)

    Now you have access to the attributes

        .. code-block:: python

            TODO: Put attributes

    """

    _device_id = ROUnaryStruct(_REG_WHOAMI, "B")

    def __init__(self, i2c_bus: I2C, address: int = _I2C_ADDR) -> NoReturn:
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._device_id != 0xA4:
            raise RuntimeError("Failed to find MC3479")
