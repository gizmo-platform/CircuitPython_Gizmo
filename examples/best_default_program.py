"""
This is the default BEST Robotics program for the Gizmo.
This program offers remote control of simple robots using 3 motors and a servo.
This may serve as a useful starting point for your team's competition code. You
will almost certainly need to edit or extend this code to meet your needs.

This code has two control modes: 'Tank Mode' and 'Arcade Mode'. The Start
button on your gamepad switches the robot between the two modes.

Here are the controls for Tank Mode:
Left Joystick Up/Down    - Motor 1 Fwd/Rev
Right Joystick Up/Down   - Motor 3 Fwd/Rev

Here are the controls for Arcade Mode:
Left Joystick Up/Down    - Robot Fwd/Rev
Left Joystick Left/Right - Robot Turn Left/Right

These controls work in both modes:
Right Trigger            - Motors 2 & 4 Forward
Right Shoulder Button    - Motors 2 & 4 Reverse
Left Trigger             - All servos to 0 degrees
Left Shoulder Button     - All servos to 90 degrees

When neither the left trigger nor shoulder button are pressed, the servo will
go to 45 degrees.
"""

import board
import digitalio
import pwmio
import time
from adafruit_motor import servo
from adafruit_simplemath import map_range, constrain
from circuitpython_gizmo import Gizmo

# the Gizmo object provides access to the data that is held by the field
# management system and the gizmo system processor
gizmo = Gizmo()

pwm_freq = 50  # Hertz
min_pulse = 1000  # milliseconds
max_pulse = 2000  # milliseconds
servo_range = 90  # degrees

# Configure the motors & servos for the ports they are connected to
motor_left = servo.ContinuousServo(
    pwmio.PWMOut(gizmo.MOTOR_1, frequency=pwm_freq),
    min_pulse=min_pulse,
    max_pulse=max_pulse
)
motor_task_a = servo.ContinuousServo(
    pwmio.PWMOut(gizmo.MOTOR_2, frequency=pwm_freq),
    min_pulse=min_pulse,
    max_pulse=max_pulse
)
motor_right = servo.ContinuousServo(
    pwmio.PWMOut(gizmo.MOTOR_3, frequency=pwm_freq),
    min_pulse=min_pulse,
    max_pulse=max_pulse
)
motor_task_b = servo.ContinuousServo(
    pwmio.PWMOut(gizmo.MOTOR_4, frequency=pwm_freq),
    min_pulse=min_pulse,
    max_pulse=max_pulse
)
servo_1 = servo.Servo(
    pwmio.PWMOut(gizmo.SERVO_1, frequency=pwm_freq),
    actuation_range=servo_range,
    min_pulse=min_pulse,
    max_pulse=max_pulse
)
servo_2 = servo.Servo(
    pwmio.PWMOut(gizmo.SERVO_2, frequency=pwm_freq),
    actuation_range=servo_range,
    min_pulse=min_pulse,
    max_pulse=max_pulse
)
servo_3 = servo.Servo(
    pwmio.PWMOut(gizmo.SERVO_3, frequency=pwm_freq),
    actuation_range=servo_range,
    min_pulse=min_pulse,
    max_pulse=max_pulse
)
servo_4 = servo.Servo(
    pwmio.PWMOut(gizmo.SERVO_4, frequency=pwm_freq),
    actuation_range=servo_range,
    min_pulse=min_pulse,
    max_pulse=max_pulse
)

# Configure the built-in LED pin as an output
builtin_led = digitalio.DigitalInOut(board.GP25)
builtin_led.direction = digitalio.Direction.OUTPUT

TANK_MODE = 0
ARCADE_MODE = 1

mode = TANK_MODE

prev_start_button = False

# Keep running forever
while True:
    # Toggle the built-in LED each second so we can see
    # that the program really is running.
    builtin_led.value = time.time() % 2 == 0

    # Refreshes the information about axis and button states
    gizmo.refresh()

    # If the start button was pressed, switch control mode
    if gizmo.buttons.start and not prev_start_button:
        if mode == TANK_MODE:
            mode = ARCADE_MODE
        elif mode == ARCADE_MODE:
            mode = TANK_MODE
    prev_start_button = gizmo.buttons.start

    if mode == TANK_MODE:
        # Convert gamepad axis positions (0 - 255) to motor speeds (-1.0 - 1.0)
        motor_left.throttle = map_range(gizmo.axes.left_y, 0, 255, -1.0, 1.0)
        motor_right.throttle = map_range(gizmo.axes.right_y, 0, 255, -1.0, 1.0)
    elif mode == ARCADE_MODE:
        # Mix right joystick axes to control both wheels
        speed = map_range(gizmo.axes.left_y, 0, 255, -1.0, 1.0)
        steering = map_range(gizmo.axes.left_x, 0, 255, -1.0, 1.0)
        motor_left.throttle = constrain(speed - steering, -1.0, 1.0)
        motor_right.throttle = constrain(speed + steering, -1.0, 1.0)

    # Control task motor with right trigger / shoulder button
    if gizmo.buttons.right_trigger:
        motor_task_a.throttle = 1.0
        motor_task_b.throttle = 1.0
    elif gizmo.buttons.right_shoulder:
        motor_task_a.throttle = -1.0
        motor_task_b.throttle = -1.0
    else:
        motor_task_a.throttle = 0.0
        motor_task_b.throttle = 0.0

    # Control task servo with left trigger / shoulder button
    if gizmo.buttons.left_trigger:
        servo_1.angle = 0
        servo_2.angle = 0
        servo_3.angle = 0
        servo_4.angle = 0
    elif gizmo.buttons.left_shoulder:
        servo_1.angle = 90
        servo_2.angle = 90
        servo_3.angle = 90
        servo_4.angle = 90
    else:
        servo_1.angle = 45
        servo_2.angle = 45
        servo_3.angle = 45
        servo_4.angle = 45
