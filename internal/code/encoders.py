from gpiozero import RotaryEncoder

from config import (
    LEFT_ENCODER_A,
    LEFT_ENCODER_B,
    RIGHT_ENCODER_A,
    RIGHT_ENCODER_B,
    ENCODER_SIGN_LEFT,
    ENCODER_SIGN_RIGHT,
    WHEEL_DIAMETER_CM,
)

from encoder_test import COUNTS_PER_REV

import math


class WheelEncoders:
    def __init__(self):
        self.left = RotaryEncoder(
            LEFT_ENCODER_A,
            LEFT_ENCODER_B
        )

        self.right = RotaryEncoder(
            RIGHT_ENCODER_A,
            RIGHT_ENCODER_B
        )

        self.left_zero = self.left.steps
        self.right_zero = self.right.steps

    # -----------------------------------------
    # Raw encoder counts
    # -----------------------------------------

    def get_left_count(self):
        raw = self.left.steps - self.left_zero
        return raw * ENCODER_SIGN_LEFT

    def get_right_count(self):
        raw = self.right.steps - self.right_zero
        return raw * ENCODER_SIGN_RIGHT

    def get_counts(self):
        return (
            self.get_left_count(),
            self.get_right_count()
        )

    # -----------------------------------------
    # Reset software zero
    # -----------------------------------------

    def reset(self):
        self.left_zero = self.left.steps
        self.right_zero = self.right.steps

    # -----------------------------------------
    # Counts -> distance
    # -----------------------------------------

    @staticmethod
    def counts_to_cm(counts):
        wheel_circumference = (
            math.pi * WHEEL_DIAMETER_CM
        )

        return (
            counts / COUNTS_PER_REV
        ) * wheel_circumference

    def get_distances_cm(self):
        left_count, right_count = self.get_counts()

        return (
            self.counts_to_cm(left_count),
            self.counts_to_cm(right_count)
        )

    # -----------------------------------------
    # Cleanup
    # -----------------------------------------

    def close(self):
        self.left.close()
        self.right.close()