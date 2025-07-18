from ultralytics import YOLO

CLASS_NAMES = {
    0: "person",
    15: "sheep",
    43: "knife",
}

SACRIFICE_CLASSES = {"person", "sheep", "knife"}

model = YOLO("yolov8x.pt")  # Load once globally


def detect_sacrifice_animal(frame):
    results = model(frame, save=False)
    detected_class_ids = [int(box[5]) for box in results[0].boxes.data]
    detected_labels = [
        CLASS_NAMES.get(cls_id, str(cls_id)) for cls_id in detected_class_ids
    ]

    return [label for label in detected_labels if label in SACRIFICE_CLASSES]
