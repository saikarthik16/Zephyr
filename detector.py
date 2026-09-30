from ultralytics import YOLO


class RescueDetector:

    def __init__(self, model_path, confidence=0.40):

        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            verbose=False
        )

        detections = []

        for result in results:

            boxes = result.boxes

            for box in boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                class_name = self.model.names[class_id]

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                detection = {
                    "class": class_name,
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2]
                }

                detections.append(detection)

        return detections