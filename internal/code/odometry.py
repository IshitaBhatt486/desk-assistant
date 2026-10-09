import math

from config import TRACK_WIDTH_CM


class Odometry:
    def __init__(self):
        self.x_cm = 0.0
        self.y_cm = 0.0
        self.theta_rad = 0.0

    def reset(self):
        self.x_cm = 0.0
        self.y_cm = 0.0
        self.theta_rad = 0.0

    def update(self, delta_left_cm, delta_right_cm):
        """
        Differential-drive odometry.

        Positive x = forward
        Positive y = left
        Positive theta = counter-clockwise / left turn
        """

        delta_s = (
            delta_left_cm + delta_right_cm
        ) / 2.0

        delta_theta = (
            delta_right_cm - delta_left_cm
        ) / TRACK_WIDTH_CM

        # Straight-line approximation
        if abs(delta_theta) < 1e-9:
            local_x = delta_s
            local_y = 0.0

        else:
            radius = delta_s / delta_theta

            local_x = (
                radius * math.sin(delta_theta)
            )

            local_y = (
                radius *
                (1.0 - math.cos(delta_theta))
            )

        cos_theta = math.cos(self.theta_rad)
        sin_theta = math.sin(self.theta_rad)

        # Transform robot-local motion into world coordinates
        self.x_cm += (
            local_x * cos_theta
            - local_y * sin_theta
        )

        self.y_cm += (
            local_x * sin_theta
            + local_y * cos_theta
        )

        self.theta_rad += delta_theta

        # Keep heading between -pi and +pi
        self.theta_rad = (
            self.theta_rad + math.pi
        ) % (2 * math.pi) - math.pi

    def get_position(self):
        return {
            "x_cm": self.x_cm,
            "y_cm": self.y_cm,
            "theta_deg": math.degrees(self.theta_rad)
        }