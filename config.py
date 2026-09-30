# Camera
CAMERA_INDEX = 0

# YOLO
MODEL_PATH = "models/rescue_model.pt"
CONFIDENCE = 0.40

# Detection classes
TARGET_CLASSES = [
    "person",
    "rubble",
    "fire",
    "smoke"
]

# MAVLink
# Change this according to your Pixhawk connection.
MAVLINK_CONNECTION = "/dev/ttyAMA0"
MAVLINK_BAUD = 57600

# Alert settings
ALERT_COOLDOWN = 10