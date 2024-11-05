import os
import uuid
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont

os.environ["QT_QPA_PLATFORM"] = "xcb"

def predict_image(filename: str) -> str:
  model: YOLO = YOLO("../model/yolo11n.pt")
  image_path: str = os.path.join(os.path.dirname(__file__), "../data", filename)
  
  results: list = model(source=image_path, conf=0.4, save=False)
  detected_objects: list = []

  for result in results:
    for detection in result.boxes:
      label = result.names[detection.cls[0].item()]
      if label in ["elephant", "person"]:
        detected_objects.append((detection.xyxy[0].tolist(), label))

  if detected_objects:
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    try:
      font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
      font = ImageFont.load_default()

    for box, label in detected_objects:
      x1, y1, x2, y2 = box
      draw.rectangle([x1, y1, x2, y2], outline="yellow", width=4)
      label_text = "Gajah" if label == "elephant" else "Manusia"
      text_position = (x1, y1 - 25)
      draw.text(text_position, label_text, fill="yellow", font=font)

    image_name: str = f"output-{uuid.uuid4().hex[:5]}.jpg"
    output_path: str = os.path.join("output", image_name)
    os.makedirs("output", exist_ok=True)
    image.save(output_path)
    print(f"Deteksi selesai dan gambar disimpan di {output_path}.")
    
    print(f"image path {image_path}")
    os.remove(image_path)
    
    return image_name
  else:
    print("Tidak ada manusia atau gajah terdeteksi, tidak ada gambar yang disimpan.")
    os.remove(image_path)
    return None
