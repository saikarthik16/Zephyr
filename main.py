import cv2
import time

from config import (
    CAMERA_INDEX,
    MODEL_PATH,
    CONFIDENCE,
    MAVLINK_CONNECTION,
    MAVLINK_BAUD,
    TARGET_CLASSES
)

from camera import RescueCamera
from detector import RescueDetector
from mavlink_gps import Pixhawk
from alerts import create_alert, print_alert


def main():

    print("Starting AI Search & Rescue Drone System")

    # -------------------------
    # Camera
    # -------------------------

    camera = RescueCamera(
        CAMERA_INDEX
    )

    # -------------------------
    # AI
    # -------------------------

    detector = RescueDetector(
        MODEL_PATH,
        CONFIDENCE
    )

    # -------------------------
    # Pixhawk
    # -------------------------

    pixhawk = Pixhawk(
        MAVLINK_CONNECTION,
        MAVLINK_BAUD
    )

    print("System ready.")

    last_alert_time = 0

    try:

        while True:

            # Get camera frame
            frame = camera.read()

            if frame is None:
                print("Camera frame unavailable")
                break

            # AI detection
            detections = detector.detect(frame)

            # Draw detections
            for detection in detections:

                class_name = detection["class"]

                confidence = detection["confidence"]

                x1, y1, x2, y2 = map(
                    int,
                    detection["bbox"]
                )

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                label = (
                    f"{class_name} "
                    f"{confidence:.2f}"
                )

                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                # Only process relevant classes
                if class_name not in TARGET_CLASSES:
                    continue

                # Prevent continuous alert spam
                current_time = time.time()

                if (
                    current_time - last_alert_time
                    < 10
                ):
                    continue

                # Get GPS
                gps = pixhawk.get_gps()

                if gps is None:

                    print(
                        "Detection found, "
                        "but GPS unavailable."
                    )

                    continue

                # Create alert
                alert = create_alert(
                    detection,
                    gps
                )

                # Display alert
                print_alert(alert)

                last_alert_time = current_time

            # Display video
            cv2.imshow(
                "AI Search & Rescue",
                frame
            )

            # Press Q to quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        camera.release()

        cv2.destroyAllWindows()

        print(
            "Search & Rescue system stopped."
        )


if __name__ == "__main__":
    main()