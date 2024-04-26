# SPDX-FileCopyrightText: Copyright (c) 2024 Gizmo Team & Contributors
#
# SPDX-License-Identifier: ISC
"""
`circuitpython_gizmo`
================================================================================

Support library for the Gizmo robotics platform.


* Author(s): Gizmo Team & Contributors
"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/gizmo-platform/CircuitPython_Gizmo.git"

import board
import busio


class GizmoButtons:
    """Holds button states from gamepad"""

    def __init__(self):
        self.x = False
        self.a = False
        self.b = False
        self.y = False
        self.left_shoulder = False
        self.right_shoulder = False
        self.left_trigger = False
        self.right_trigger = False
        self.back = False
        self.start = False
        self.left_stick = False
        self.right_stick = False

    def update(self, data):
        """Parses state from raw bytes

        :param bytearray data: The full i2c data buffer
        """
        self.x = data[6] > 0
        self.a = data[7] > 0
        self.b = data[8] > 0
        self.y = data[9] > 0
        self.left_shoulder = data[10] > 0
        self.right_shoulder = data[11] > 0
        self.left_trigger = data[12] > 0
        self.right_trigger = data[13] > 0
        self.back = data[14] > 0
        self.start = data[15] > 0
        self.left_stick = data[16] > 0
        self.right_stick = data[17] > 0


class GizmoAxes:
    """Holds axis states from gamepad"""

    def __init__(self):
        self.left_x = 127
        self.left_y = 127
        self.right_x = 127
        self.right_y = 127
        self.dpad_x = 127
        self.dpad_y = 127

    def update(self, data):
        """Parses state from raw bytes

        :param bytearray data: The full i2c data buffer
        """
        self.left_x = data[0]
        self.left_y = data[1]
        self.right_x = data[2]
        self.right_y = data[3]
        self.dpad_x = data[4]
        self.dpad_y = data[5]


class Gizmo:
    """Gizmo interface object"""

    MOTOR_1 = board.GP14
    MOTOR_2 = board.GP15
    MOTOR_3 = board.GP16
    MOTOR_4 = board.GP17
    MOTOR_5 = board.GP18
    MOTOR_6 = board.GP19
    MOTOR_7 = board.GP20
    MOTOR_8 = board.GP21

    GPIO_1 = board.GP6
    GPIO_2 = board.GP7
    GPIO_3 = board.GP8
    GPIO_4 = board.GP9
    GPIO_5 = board.GP10
    GPIO_6 = board.GP11
    GPIO_7 = board.GP12
    GPIO_8 = board.GP13

    ADC_1 = board.GP26_A0
    ADC_2 = board.GP27_A1
    ADC_3 = board.GP28_A2

    UART_TX = board.GP4
    UART_RX = board.GP5

    NEOPIXEL = board.GP22

    def __init__(self) -> None:
        self.axes = GizmoAxes()
        self.buttons = GizmoButtons()
        self.i2c_buffer = bytearray(18)
        try:
            self.i2c = busio.I2C(sda=board.GP2, scl=board.GP3)
            while self.i2c.try_lock():
                pass
        except RuntimeError:
            print(
                "Warning: Could not connect to system processor. This is normal if "
                "your Gizmo is not connected to a battery."
            )
            self.i2c = None

    def __enter__(self) -> "Gizmo":
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.deinit()

    def deinit(self):
        """Releases lock on I2C device"""
        if self.i2c is not None:
            self.i2c.unlock()

    def refresh(self) -> None:
        """Polls system processor for latest gamepad state"""
        if self.i2c is None:
            return
        try:
            self.i2c.readfrom_into(8, self.i2c_buffer)
            self.axes.update(self.i2c_buffer)
            self.buttons.update(self.i2c_buffer)
        except OSError:
            self.axes.update([127] * 6)
            self.buttons.update([0] * 12)
