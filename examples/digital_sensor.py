"""
This example shows how to read a sensor connected to a digital (GPIO) port.
"""

import digitalio
import time
from circuitpython_gizmo import Gizmo

gizmo = Gizmo()

sensor = digitalio.DigitalInOut(gizmo.GPIO_1)

while True:
    print(sensor.value)
    time.sleep(0.1)
