from ultralytics import YOLO
from PIL import Image
from io import BytesIO
import requests

class Proton:

    def __init__(self):
        self._model = "ProtonCaptcha.pt"

    def solve(self, image_url: str) -> dict:
         
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        model = YOLO(self._model)
        results = model.predict(image)

        if len(results[0].boxes) == 0:
            raise Exception("No objects found on the image")

        bbox = results[0].boxes[0].xyxy[0]

        x_center = (bbox[0] + bbox[2]) / 2
        y_center = (bbox[1] + bbox[3]) / 2

        return float(x_center), float(y_center)