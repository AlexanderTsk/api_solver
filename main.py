from fastapi import FastAPI
from pydantic import BaseModel
from proton import Proton
from google import Google

app = FastAPI()

class GoogleCaptchaModel(BaseModel):
    image_url: str
    target: str
    type: str

class ProtonCaptchaModel(BaseModel):
    image_url: str

@app.post("/google")
def solve_google(data: GoogleCaptchaModel):
    google = Google()
    answers = google.solve(data.image_url, data.target, data.type)

    return {"answers": answers}

@app.post("/proton")
def solve_proton(data: ProtonCaptchaModel):
    proton = Proton()
    x, y = proton.solve(data.image_url)

    return {'x': float(x), 'y': float(y)}

