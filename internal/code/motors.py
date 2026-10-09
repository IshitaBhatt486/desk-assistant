from gpiozero import PWMOutputDevice, DigitalOutputDevice

from config import (
    LEFT_EN,
    LEFT_IN1,
    LEFT_IN2,
    RIGHT_EN,
    RIGHT_IN1,
    RIGHT_IN2,
    LEFT_MOTOR_INVERTED,
    RIGHT_MOTOR_INVERTED,
    PWM_FREQUENCY,
)


class Motor:
    def __init__(
        self,
        enable_pin,
        in1_pin,
        in2_pin,
        inverted=False
    ):
        self.enable = PWMOutputDevice(
            enable_pin,
            frequency=PWM_FREQUENCY,
            initial_value=0
        )

        self.in1 = DigitalOutputDevice(in1_pin)
        self.in2 = DigitalOutputDevice(in2_pin)

        self.inverted = inverted

    def set_speed(self, speed):
        """
        speed:
            -100 = full reverse
             0   = stop
            +100 = full forward
        """

        speed = max(-100.0, min(100.0, speed))

        if self.inverted:
            speed = -speed

        if speed > 0:
            self.in1.on()
            self.in2.off()
            self.enable.value = speed / 100.0

        elif speed < 0:
            self.in1.off()
            self.in2.on()
            self.enable.value = abs(speed) / 100.0

        else:
            self.enable.value = 0
            self.in1.off()
            self.in2.off()

    def stop(self):
        self.set_speed(0)

    def close(self):
        self.stop()
        self.enable.close()
        self.in1.close()
        self.in2.close()


class DualMotorController:
    def __init__(self):
        self.left = Motor(
            LEFT_EN,
            LEFT_IN1,
            LEFT_IN2,
            LEFT_MOTOR_INVERTED
        )

        self.right = Motor(
            RIGHT_EN,
            RIGHT_IN1,
            RIGHT_IN2,
            RIGHT_MOTOR_INVERTED
        )

    def set_speeds(self, left_speed, right_speed):
        self.left.set_speed(left_speed)
        self.right.set_speed(right_speed)

    def stop(self):
        self.left.stop()
        self.right.stop()

    def close(self):
        self.left.close()
        self.right.close()