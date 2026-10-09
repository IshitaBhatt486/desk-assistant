
from gpiozero import Motor
from time import sleep

# Left motor: IN1, IN2, enable
left_motor = Motor(
    forward=17,
    backward=27,
    enable=12
)

# Right motor: IN1, IN2, enable
right_motor = Motor(
    forward=22,
    backward=23,
    enable=6
)

try:
    print("Moving forward")
    left_motor.forward(0.5)
    right_motor.forward(0.5)
    sleep(2)

    print("Stopping")
    left_motor.stop()
    right_motor.stop()
    sleep(1)

    print("Moving backward")
    left_motor.backward(0.5)
    right_motor.backward(0.5)
    sleep(2)

    print("Stopping")
    left_motor.stop()
    right_motor.stop()

finally:
    left_motor.close()
    right_motor.close()