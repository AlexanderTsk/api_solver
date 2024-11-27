# Proton and Gooogle reCaptcha v3 solver

This python project allows you to solve 2 different types of captcha. The first one is Proton captcha where you need to drug and drop the puzzle inside html canvas. The second one is Google reCaptcha v3 where you need to pick correct image from giving task.

## Features

- Detect Proton captcha answer coordinates where you need to move the puzzle.
- Detect Google captca answears.

## Requirements

- Python 3.8+
- Trained YOLO models for Google and Proton answers detection.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/AlexanderTsk/api_solver.git
   cd api_solver

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run command:
   ```bash
   uvicorn main:app --reload

## Usage 
Open the link http://127.0.0.1:8000/docs. Here you can test how API works. 

1. For Proton captcha solwing use <u>/proton</u> endpoint. You just need to send image URL where full canvas is present. The API will return you x and y coordinates of the answer center. Use this coordinates to drag and drop your Puzzle pice

1. For Google captcha solwing use <u>/google</u> endpoint. Here you need 3 values. 1) Image URL which you need to take from the google captcha HTML <b>img</b> tag with class name "rc-image". 2) The target you can take from the "rc-imageselect-desc-no-canonical" <b>div</b> tag. This is the object which you should find on the provided image. 3) The type field is the google recaptcha type. This code allows you to solve only 2/3 types (default and square). The default captcha type it is a captcha where you need to choose correct answers from 3x3 matrix and press <u>Verify</u> button. The squre captcha it is a captcha where you need to select objects on the 4x4 matrix.