"""
Encoder calibration/test.

Run:
    python encoder_test.py

Rotate each wheel a known number of complete revolutions.
The program calculates the measured counts/revolution.

After calibration, replace COUNTS_PER_REV below
with the measured value.
"""

import time
from gpiozero import RotaryEncoder

from config import (
    LEFT_ENCODER_A,
    LEFT_ENCODER_B,
    RIGHT_ENCODER_A,
    RIGHT_ENCODER_B,
)


# =========================================================
# IMPORTANT:
# Put your calibrated counts-per-wheel-revolution here.
#
# 600 is only a PLACEHOLDER.
# Replace it with the value obtained from this test.
# =========================================================
COUNTS_PER_REV = 600

# Number of physical wheel revolutions used for calibration
CALIBRATION_REVOLUTIONS = 10


def calibrate_encoder(name, encoder):
    print()
    print(f"--- {name} encoder ---")
    print(
        f"Current configured COUNTS_PER_REV = {COUNTS_PER_REV}"
    )

    input(
        f"Rotate the {name.lower()} wheel "
        f"exactly {CALIBRATION_REVOLUTIONS} complete revolutions, "
        f"then press ENTER..."
    )

    start_count = encoder.steps

    input(
        f"Now rotate the {name.lower()} wheel "
        f"exactly {CALIBRATION_REVOLUTIONS} complete revolutions "
        f"and press ENTER..."
    )

    end_count = encoder.steps

    measured_counts = abs(end_count - start_count)

    measured_cpr = (
        measured_counts / CALIBRATION_REVOLUTIONS
    )

    print()
    print(f"{name} encoder:")
    print(f"Measured counts = {measured_counts}")
    print(f"Revolutions     = {CALIBRATION_REVOLUTIONS}")
    print(f"Counts/rev      = {measured_cpr:.2f}")

    return measured_cpr


def live_test(encoder, name):
    print()
    print(f"Live test: {name}")
    print("Rotate the wheel manually.")
    print("Press Ctrl+C to stop.")

    last = encoder.steps

    try:
        while True:
            current = encoder.steps

            if current != last:
                print(
                    f"{name}: "
                    f"counts={current}, "
                    f"delta={current - last}"
                )

                last = current

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nLive test stopped.")


def main():
    left_encoder = RotaryEncoder(
        LEFT_ENCODER_A,
        LEFT_ENCODER_B
    )

    right_encoder = RotaryEncoder(
        RIGHT_ENCODER_A,
        RIGHT_ENCODER_B
    )

    print("======================================")
    print("        ENCODER TEST / CALIBRATION")
    print("======================================")

    print(f"\nCurrent COUNTS_PER_REV = {COUNTS_PER_REV}")

    try:
        left_cpr = calibrate_encoder("LEFT", left_encoder)
        right_cpr = calibrate_encoder("RIGHT", right_encoder)

        average_cpr = (left_cpr + right_cpr) / 2

        print("\n======================================")
        print("CALIBRATION RESULT")
        print("======================================")

        print(f"Left counts/rev   = {left_cpr:.2f}")
        print(f"Right counts/rev  = {right_cpr:.2f}")
        print(f"Average           = {average_cpr:.2f}")

        print("\nPut this value into encoder_test.py:")
        print(f"\nCOUNTS_PER_REV = {round(average_cpr)}")

        print(
            "\nIf left and right are significantly different, "
            "do not blindly average them."
        )
    finally:
        left_encoder.close()
        right_encoder.close()


if __name__ == "__main__":
    main()
