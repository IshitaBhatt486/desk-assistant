# gives the API

# robot.forward(30, 25)
# robot.backward(20, 20)
# robot.turn(90, 25)
# robot.left(90, 20)
# robot.right(45, 20)

from motors import DualMotorController
from encoders import WheelEncoders
from odometry import Odometry
from movement import MovementController


class Robot:
    def __init__(self):
        self.motors = DualMotorController()
        self.encoders = WheelEncoders()
        self.odometry = Odometry()

        self.movement = MovementController(
            self.motors,
            self.encoders,
            self.odometry
        )

    # ==========================================
    # Movement API
    # ==========================================

    def forward(self, amount_cm, speed=25):
        self.movement.move_distance(
            amount_cm,
            speed
        )

    def backward(self, amount_cm, speed=25):
        self.movement.move_distance(
            -abs(amount_cm),
            speed
        )

    def turn(self, angle_deg, speed=20):
        self.movement.turn(
            angle_deg,
            speed
        )

    def left(self, angle_deg=90, speed=20):
        self.turn(
            abs(angle_deg),
            speed
        )

    def right(self, angle_deg=90, speed=20):
        self.turn(
            -abs(angle_deg),
            speed
        )

    def stop(self):
        self.motors.stop()

    # ==========================================
    # Odometry
    # ==========================================

    def position(self):
        return self.odometry.get_position()

    def reset_odometry(self):
        self.odometry.reset()

    # ==========================================
    # Cleanup
    # ==========================================

    def close(self):
        self.motors.close()
        self.encoders.close()