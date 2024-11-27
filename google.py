from torch import Tensor
from ultralytics import YOLO
from PIL import Image
from io import BytesIO
import numpy as np
import re
import requests

class Google:

    def __init__(self):
        self._model = "GoogleCaptcha.pt"

    def solve(self, image_url: str, target: str, type: str) -> list:
         
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        model = YOLO(self._model)
        result = model.predict(image)

        target_num = self._get_google_captcha_target_num(target)

        if target_num == 1000:
            return list()

        target_index = []
        count = 0
        for num in result[0].boxes.cls:
            if num == target_num:
                target_index.append(count)
            count += 1

        boxes = result[0].boxes.data

        if(type == 'default'):
            return self._get_google_captcha_answer(target_index, boxes)
        
        if(type == 'square'):
            return self._get_google_captcha_answer4(target_index, boxes)

        return list()

       
    
    def _get_google_captcha_target_num(self, target: str) -> int:
        
        if re.search(r"bicycle", target) != None:
            return 0
        elif re.search(r"boat", target) != None:
            return 1
        elif re.search(r"bridge", target) != None:
            return 2
        elif re.search(r"bus", target) != None:
            return 3
        elif re.search(r"car", target) != None:
            return 4
        elif re.search(r"chimney", target) != None:
            return 5
        elif re.search(r"crosswalk", target) != None:
            return 6
        elif re.search(r"hydrant", target) != None:
            return 7
        elif re.search(r"motorcycle", target) != None:
            return 8
        elif re.search(r"stair", target) != None:
            return 9
        elif re.search(r"traffic light", target) != None:
            return 10
        elif re.search(r"tree", target) != None:
            return 11
        else:
            return 1000
    
    def _get_google_captcha_answer(self, target_index: list, boxes: Tensor | np.ndarray) -> list:
        
        answers = []
        count = 0
        for i in target_index:
            target_box = boxes[i]
            p1, p2 = (int(target_box[0]), int(target_box[1])
                        ), (int(target_box[2]), int(target_box[3]))
            x1, y1 = p1
            x2, y2 = p2

            xc = (x1+x2)/2
            yc = (y1+y2)/2

            if xc < 100 and yc < 100:
                answers.append(1)
            if 100 < xc < 200 and yc < 100:
                answers.append(2)
            if 200 < xc < 300 and yc < 100:
                answers.append(3)

            if xc < 100 and 100 < yc < 200:
                answers.append(4)
            if 100 < xc < 200 and 100 < yc < 200:
                answers.append(5)
            if 200 < xc < 300 and 100 < yc < 200:
                answers.append(6)

            if xc < 100 and 200 < yc < 300:
                answers.append(7)
            if 100 < xc < 200 and 200 < yc < 300:
                answers.append(8)
            if 200 < xc < 300 and 200 < yc < 300:
                answers.append(9)

            count += 1

        return list(set(answers))

    def _get_google_captcha_answer4(self, target_index: list, boxes: Tensor | np.ndarray) -> list:
        
        answers = []
        count = 0
        for i in target_index:
            target_box = boxes[i]
            p1, p2 = (int(target_box[0]), int(target_box[1])
                    ), (int(target_box[2]), int(target_box[3]))
            x1, y1 = p1
            x4, y4 = p2
            x2 = x4
            y2 = y1
            x3 = x1
            y3 = y4
            xys = [x1, y1, x2, y2, x3, y3, x4, y4]

            four_cells = []
            for i in range(4):
                x = xys[i*2]
                y = xys[(i*2)+1]

                if x < 112.5 and y < 112.5:
                    four_cells.append(1)
                if 112.5 < x < 225 and y < 112.5:
                    four_cells.append(2)
                if 225 < x < 337.5 and y < 112.5:
                    four_cells.append(3)
                if 337.5 < x <= 450 and y < 112.5:
                    four_cells.append(4)

                if x < 112.5 and 112.5 < y < 225:
                    four_cells.append(5)
                if 112.5 < x < 225 and 112.5 < y < 225:
                    four_cells.append(6)
                if 225 < x < 337.5 and 112.5 < y < 225:
                    four_cells.append(7)
                if 337.5 < x <= 450 and 112.5 < y < 225:
                    four_cells.append(8)

                if x < 112.5 and 225 < y < 337.5:
                    four_cells.append(9)
                if 112.5 < x < 225 and 225 < y < 337.5:
                    four_cells.append(10)
                if 225 < x < 337.5 and 225 < y < 337.5:
                    four_cells.append(11)
                if 337.5 < x <= 450 and 225 < y < 337.5:
                    four_cells.append(12)

                if x < 112.5 and 337.5 < y <= 450:
                    four_cells.append(13)
                if 112.5 < x < 225 and 337.5 < y <= 450:
                    four_cells.append(14)
                if 225 < x < 337.5 and 337.5 < y <= 450:
                    four_cells.append(15)
                if 337.5 < x <= 450 and 337.5 < y <= 450:
                    four_cells.append(16)
            answer = self._get_occupied_cells(four_cells)
            count += 1
            for ans in answer:
                answers.append(ans)
        answers = sorted(list(answers))
        return list(set(answers))
    
    def _get_occupied_cells(self, vertices):
        occupied_cells = set()
        rows, cols = zip(*[((v-1)//4, (v-1) % 4) for v in vertices])

        for i in range(min(rows), max(rows)+1):
            for j in range(min(cols), max(cols)+1):
                occupied_cells.add(4*i + j + 1)

        return sorted(list(occupied_cells))