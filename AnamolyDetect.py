from ultralytics import YOLO
import cv2

class Prg:
    def __init__(self):
        self.model = YOLO("yolov9c.pt")

    def CountHeadDetectWeapon(self, frame):
        results = self.model(frame,verbose = False)
        weapon_labels=["gun", "rifle", "knife", "pistol", "shotgun", "machine gun", "grenade", "sword", "dagger", "revolver"]
        weapon_present=False

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = box.cls[0]
                label = self.model.names[int(cls)]
                if label in weapon_labels:
                    label = f"{label} {conf:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.9,
                        (255, 0, 0),
                        2,
                    )
                    weapon_present=True
        count = 0
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = box.cls[0]
                if self.model.names[int(cls)] == "person":
                    count += 1
                    label = f"Person {conf:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.9,
                        (0, 255, 0),
                        2,
                    )
        cv2.putText(
            frame,
            f"Head Count: {count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )
        return frame, count, weapon_present
