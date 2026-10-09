import math
import time

from config import (
    WHEEL_DIAMETER_CM,
    TRACK_WIDTH_CM,
    CONTROL_PERIOD_S,
    ACCELERATION_RATE,
    DECELERATION_RATE,
    DECELERATION_DISTANCE_CM,
    MIN_CREEP_SPEED,
    MAX_CORRECTION_PERCENT,
    KP_STRAIGHT,
    TURN_SCALE,
    MOVE_TIMEOUT_S,
    TURN_TIMEOUT_S,
)

from encoder_test import COUNTS_PER_REV


def clamp(value, low, high):
    return max(low, min(high, value))


class MovementController:
    def __init__(self, motors, encoders, odometry):
        self.motors = motors
        self.encoders = encoders
        self.odometry = odometry

    # ==================================================
    # Utility
    # ==================================================

    def _counts_to_cm(self, counts):
        circumference = math.pi * WHEEL_DIAMETER_CM

        return (
            counts / COUNTS_PER_REV
        ) * circumference

    def _ramp_speed(
        self,
        current,
        target,
        dt
    ):
        if target > current:
            change = ACCELERATION_RATE * dt
            return min(current + change, target)

        change = DECELERATION_RATE * dt
        return max(current - change, target)

    # ==================================================
    # STRAIGHT MOVEMENT
    # ==================================================

    def move_distance(self, distance_cm, speed):
        """
        Move forward/backward by distance_cm.

        Examples:
            move_distance(30, 25)
            move_distance(-20, 30)
        """

        if distance_cm == 0:
            self.motors.stop()
            return

        speed = clamp(abs(speed), 0, 100)

        direction = (
            1 if distance_cm > 0 else -1
        )

        target_distance_cm = abs(distance_cm)

        target_counts = (
            target_distance_cm
            / (math.pi * WHEEL_DIAMETER_CM)
            * COUNTS_PER_REV
        )

        self.encoders.reset()

        current_speed = 0.0

        previous_left_cm = 0.0
        previous_right_cm = 0.0

        start_time = time.monotonic()

        try:
            while True:

                # --------------------------------------
                # Encoder readings
                # --------------------------------------

                left_count, right_count = (
                    self.encoders.get_counts()
                )

                # Make progress positive even when moving backward
                left_progress_counts = (
                    left_count * direction
                )

                right_progress_counts = (
                    right_count * direction
                )

                average_progress_counts = (
                    left_progress_counts
                    + right_progress_counts
                ) / 2.0

                # --------------------------------------
                # Convert to distance
                # --------------------------------------

                left_progress_cm = self._counts_to_cm(
                    left_progress_counts
                )

                right_progress_cm = self._counts_to_cm(
                    right_progress_counts
                )

                average_progress_cm = (
                    left_progress_cm
                    + right_progress_cm
                ) / 2.0

                # --------------------------------------
                # Odometry
                # --------------------------------------

                actual_left_cm = self._counts_to_cm(
                    left_count
                )

                actual_right_cm = self._counts_to_cm(
                    right_count
                )

                delta_left_cm = (
                    actual_left_cm
                    - previous_left_cm
                )

                delta_right_cm = (
                    actual_right_cm
                    - previous_right_cm
                )

                self.odometry.update(
                    delta_left_cm,
                    delta_right_cm
                )

                previous_left_cm = actual_left_cm
                previous_right_cm = actual_right_cm

                # --------------------------------------
                # Finish condition
                # --------------------------------------

                if average_progress_counts >= target_counts:
                    break

                # --------------------------------------
                # Timeout safety
                # --------------------------------------

                if (
                    time.monotonic() - start_time
                    > MOVE_TIMEOUT_S
                ):
                    raise RuntimeError(
                        "Movement timed out. "
                        "Check encoder wiring/counts."
                    )

                # --------------------------------------
                # Remaining distance
                # --------------------------------------

                remaining_cm = max(
                    0.0,
                    target_distance_cm
                    - average_progress_cm
                )

                # --------------------------------------
                # Deceleration
                # --------------------------------------

                target_speed = speed

                if (
                    remaining_cm
                    < DECELERATION_DISTANCE_CM
                ):
                    ratio = (
                        remaining_cm
                        / DECELERATION_DISTANCE_CM
                    )

                    target_speed = max(
                        MIN_CREEP_SPEED,
                        speed * ratio
                    )

                # --------------------------------------
                # Acceleration/deceleration ramp
                # --------------------------------------

                current_speed = self._ramp_speed(
                    current_speed,
                    target_speed,
                    CONTROL_PERIOD_S
                )

                # --------------------------------------
                # Straight-line correction
                # --------------------------------------

                error_cm = (
                    left_progress_cm
                    - right_progress_cm
                )

                correction = (
                    KP_STRAIGHT * error_cm
                )

                correction = clamp(
                    correction,
                    -MAX_CORRECTION_PERCENT,
                    MAX_CORRECTION_PERCENT
                )

                left_speed = (
                    current_speed - correction
                )

                right_speed = (
                    current_speed + correction
                )

                left_speed = clamp(
                    left_speed,
                    0,
                    100
                )

                right_speed = clamp(
                    right_speed,
                    0,
                    100
                )

                # Apply movement direction
                left_command = (
                    direction * left_speed
                )

                right_command = (
                    direction * right_speed
                )

                self.motors.set_speeds(
                    left_command,
                    right_command
                )

                time.sleep(CONTROL_PERIOD_S)

        finally:
            self.motors.stop()

    # ==================================================
    # TURN
    # ==================================================

    def turn(self, angle_deg, speed):
        """
        Turn in place.

        +angle = left / counter-clockwise
        -angle = right / clockwise

        Example:
            turn(90, 20)
            turn(-90, 20)
        """

        if angle_deg == 0:
            self.motors.stop()
            return

        speed = clamp(abs(speed), 0, 100)

        angle_rad = math.radians(angle_deg)

        # Distance each wheel must travel
        wheel_distance_cm = (
            abs(angle_rad)
            * TRACK_WIDTH_CM
            / 2.0
        )

        wheel_distance_cm *= TURN_SCALE

        target_counts = (
            wheel_distance_cm
            / (math.pi * WHEEL_DIAMETER_CM)
            * COUNTS_PER_REV
        )

        # Positive angle = left turn
        if angle_deg > 0:
            left_direction = -1
            right_direction = 1
        else:
            left_direction = 1
            right_direction = -1

        self.encoders.reset()

        current_speed = 0.0

        previous_left_cm = 0.0
        previous_right_cm = 0.0

        start_time = time.monotonic()

        try:
            while True:

                # --------------------------------------
                # Encoder counts
                # --------------------------------------

                left_count, right_count = (
                    self.encoders.get_counts()
                )

                left_progress_counts = (
                    left_count * left_direction
                )

                right_progress_counts = (
                    right_count * right_direction
                )

                average_progress_counts = (
                    left_progress_counts
                    + right_progress_counts
                ) / 2.0

                # --------------------------------------
                # Convert to cm
                # --------------------------------------

                left_progress_cm = (
                    self._counts_to_cm(
                        left_progress_counts
                    )
                )

                right_progress_cm = (
                    self._counts_to_cm(
                        right_progress_counts
                    )
                )

                average_progress_cm = (
                    left_progress_cm
                    + right_progress_cm
                ) / 2.0

                # --------------------------------------
                # Odometry
                # --------------------------------------

                actual_left_cm = (
                    self._counts_to_cm(left_count)
                )

                actual_right_cm = (
                    self._counts_to_cm(right_count)
                )

                delta_left_cm = (
                    actual_left_cm
                    - previous_left_cm
                )

                delta_right_cm = (
                    actual_right_cm
                    - previous_right_cm
                )

                self.odometry.update(
                    delta_left_cm,
                    delta_right_cm
                )

                previous_left_cm = actual_left_cm
                previous_right_cm = actual_right_cm

                # --------------------------------------
                # Finish
                # --------------------------------------

                if (
                    average_progress_counts
                    >= target_counts
                ):
                    break

                if (
                    time.monotonic() - start_time
                    > TURN_TIMEOUT_S
                ):
                    raise RuntimeError(
                        "Turn timed out. "
                        "Check encoder wiring, "
                        "COUNTS_PER_REV and TRACK_WIDTH_CM."
                    )

                # --------------------------------------
                # Deceleration
                # --------------------------------------

                remaining_cm = max(
                    0.0,
                    wheel_distance_cm
                    - average_progress_cm
                )

                target_speed = speed

                if (
                    remaining_cm
                    < DECELERATION_DISTANCE_CM
                ):
                    ratio = (
                        remaining_cm
                        / DECELERATION_DISTANCE_CM
                    )

                    target_speed = max(
                        MIN_CREEP_SPEED,
                        speed * ratio
                    )

                current_speed = self._ramp_speed(
                    current_speed,
                    target_speed,
                    CONTROL_PERIOD_S
                )

                # --------------------------------------
                # Keep both wheels synchronized
                # --------------------------------------

                error_cm = (
                    left_progress_cm
                    - right_progress_cm
                )

                correction = (
                    KP_STRAIGHT * error_cm
                )

                correction = clamp(
                    correction,
                    -MAX_CORRECTION_PERCENT,
                    MAX_CORRECTION_PERCENT
                )

                left_speed = clamp(
                    current_speed - correction,
                    0,
                    100
                )

                right_speed = clamp(
                    current_speed + correction,
                    0,
                    100
                )

                self.motors.set_speeds(
                    left_direction * left_speed,
                    right_direction * right_speed
                )

                time.sleep(CONTROL_PERIOD_S)

        finally:
            self.motors.stop()