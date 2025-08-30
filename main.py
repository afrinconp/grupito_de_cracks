from ultralytics import YOLO

# Load an Open Images Dataset V7 pretrained YOLOv8n model
model = YOLO("yolov8n-oiv7.pt")

# Run prediction
results = model.predict(source="onions.jpg")

# Print the class names YOLO detected in the image
for r in results:
    names = [r.names[int(c)] for c in r.boxes.cls]  # convert class IDs to names
    print(f"{r.path} -> {', '.join(names)}")