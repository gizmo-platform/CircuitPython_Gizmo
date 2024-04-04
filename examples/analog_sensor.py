"""
This example shows how to read a sensor connected to an analog port.
"""

import analogio
import time
from circuitpython_gizmo import Gizmo

gizmo = Gizmo()

sensor = analogio.AnalogIn(gizmo.ADC_1)

while True:
    print(sensor.value)
    time.sleep(0.1)
