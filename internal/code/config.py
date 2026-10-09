# ============================================
# Raspberry Pi GPIO configuration
# BCM GPIO numbering
# ============================================

# ---------- L298N ----------
LEFT_EN = 12       # Physical pin 12
LEFT_IN1 = 17      # Physical pin 16
LEFT_IN2 = 27      # Physical pin 18

RIGHT_EN = 19      # Physical pin 35
RIGHT_IN1 = 22     # Physical pin 13
RIGHT_IN2 = 13     # Physical pin 15


# ---------- Encoders ----------
LEFT_ENCODER_A = 5     # Physical pin 29
LEFT_ENCODER_B = 5     # Physical pin 31

RIGHT_ENCODER_A = 6   # Physical pin 33
RIGHT_ENCODER_B = 6   # Physical pin 36


# ---------- Motor direction ----------
# Keep/change these according to the motor wiring
# from your Step 1 setup.

LEFT_MOTOR_INVERTED = False
RIGHT_MOTOR_INVERTED = True


# ---------- Encoder direction ----------
# After testing:
# +1 = encoder count increases when wheel moves forward
# -1 = encoder count decreases when wheel moves forward

ENCODER_SIGN_LEFT = 1
ENCODER_SIGN_RIGHT = 1


# ---------- Physical robot dimensions ----------
# REPLACE these with your measured values.

WHEEL_DIAMETER_CM = 6.5
TRACK_WIDTH_CM = 14.0


# ---------- Control ----------
PWM_FREQUENCY = 1000

CONTROL_PERIOD_S = 0.02       # 50 Hz control loop

ACCELERATION_RATE = 60.0      # % speed / second
DECELERATION_RATE = 100.0     # % speed / second

DECELERATION_DISTANCE_CM = 10.0
MIN_CREEP_SPEED = 12.0

MAX_CORRECTION_PERCENT = 20.0

# Straight-line correction gain.
# Increase if correction is too weak.
# Decrease if robot oscillates.
KP_STRAIGHT = 2.0

# Turn calibration factor.
# Start at 1.0.
# Example: if commanded 90° gives 84°, increase slightly.
TURN_SCALE = 1.0

# Safety timeout
MOVE_TIMEOUT_S = 60.0
TURN_TIMEOUT_S = 30.0