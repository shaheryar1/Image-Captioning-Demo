from fastapi import FastAPI,File, UploadFile
import numpy as np
import io
import base64
from PIL import Image
from caption import *
import cv2
import base64







def encode(img):
    pil_img = Image.fromarray(img)
    buff = io.BytesIO()
    pil_img.save(buff, format="JPEG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    return  new_image_string


app = FastAPI()


@app.post("/generate_caption")
async def root(file: bytes = File(...)):
    print("abc")
    image = Image.open(io.BytesIO(file)).convert("RGB")
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite('a.jpg',img)
    word_arr = generate_caption('a.jpg',5)
    capation=""
    for word in word_arr[1:-1]:
        capation=capation+word+" "
    capation=str.strip(capation)
    return {"caption":capation}
