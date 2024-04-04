# Gizmo for CircuitPython

This repo contains the CircuitPython library that allows you to
program your gizmo controller using the CircuitPython environment.

## Prerequisites

You must have installed and configured
[CircuitPython](https://circuitpython.org/).

Some examples use libraries from the
[Adafruit Bundle](https://circuitpython.org/libraries).

Some examples use the
[adafruit_simplemath module](https://github.com/adafruit/Adafruit_CircuitPython_SimpleMath).
This can be installed following a similar process as is
outlined below.

## Installation

### Manual Installation

To manually install the Gizmo library onto your CircuitPython
device:

1. Download the mpy bundle from the
[latest release](https://github.com/gizmo-platform/CircuitPython_Gizmo/releases/latest).
1. Extract the ZIP file on your computer.
1. Copy "circuitpython_gizmo.mpy" from the "lib" folder of the
extracted zip to the "lib" folder of your "CIRCUITPY" drive.

### CircUp Installation

To install the Gizmo library using the
[CircUp](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/overview)
tool:

1. Add the bundle to your local list.

    ```Shell
    circup bundle-add gizmo-platform/CircuitPython_Gizmo
    ```

1. Install the module to your connected device.

    ```Shell
    circup install circuitpython_gizmo
    ```

## Usage

Access to Gizmo features is provided through the `Gizmo` class.

```Python
from circuitpython_gizmo import Gizmo

gizmo = Gizmo()
```

You can access the gamepad state with `gizmo.buttons` and
`gizmo.axes`.

```Python
# True if the A button is pressed. False if not.
gizmo.buttons.a

# Position of the left vertical stick from 0 to 255
gizmo.axes.left_y
```

You must call `gizmo.refresh()` at a regular interval to get
the latest information from the Gizmo. Most Gizmo programs will
have this structure:

```Python
from circuitpython_gizmo import Gizmo
# other imports...

gizmo = Gizmo()

# setup motors / sensors...

while True:
    gizmo.refresh()

    # do robot tasks...
```

Finally, the Gizmo class has variables you can use to refer to
specific ports on the Gizmo board when working with other
CircuitPython features. For example, `gizmo.MOTOR_1` refers to
motor port 1 on the Gizmo board and can be used with the
`pwmio` module to control Gizmo motors.

```Python
# Control motor port 1 as a PWM output
motor_pwm = pwmio.PWMOut(gizmo.MOTOR_1, frequency=50)
```

See the examples folder for complete code files demonstrating
how to use this library.
