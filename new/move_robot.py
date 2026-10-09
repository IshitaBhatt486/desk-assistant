from gpiozero import Motor
from time import sleep

left_motor = Motor(forward=27, backward=17, enable=12)
right_motor = Motor(forward=23, backward=22, enable=6)

def move_forward():
    left_motor.forward(0.5)
    right_motor.forward(0.5)

def move_backward():
    left_motor.backward(0.5)
    right_motor.backward(0.5)

def turn_left():
    left_motor.backward(0.5)
    right_motor.forward(0.5)
    sleep(0.7)  # Adjust for a 90-degree turn
    stop()

def turn_right():
    left_motor.forward(0.5)
    right_motor.backward(0.5)
    sleep(0.7)  # Adjust for a 90-degree turn
    stop()

def stop():
    left_motor.stop()
    right_motor.stop()

try:
    print("Forward")
    move_forward()
    sleep(2)
    stop()
    sleep(1)

    print("Backward")
    move_backward()
    sleep(2)
    stop()
    sleep(1)

    print("Turn left 90 degrees")
    turn_left()
    sleep(1)

    print("Forward")
    move_forward()
    sleep(2)
    stop()
    sleep(1)

    print("Backward")
    move_backward()
    sleep(2)
    stop()
    sleep(1)

    print("Turn right 90 degrees")
    turn_right()
    sleep(1)

    print("Forward")
    move_forward()
    sleep(2)
    stop()
    sleep(1)

    print("Backward")
    move_backward()
    sleep(2)
    stop()

finally:
    stop()
    left_motor.close()
    right_motor.close()