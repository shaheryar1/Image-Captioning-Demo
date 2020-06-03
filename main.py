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
    try:
        image = Image.open(io.BytesIO(file)).convert("RGB")
        img = np.array(image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite('a.jpg',img)
        res = generate_caption('a.jpg',1)
        caption = ""
        words = []
        for word, score in zip(res["words"],res["scores"]):
            caption = caption + " " + word
            print(word, score)
            word = {
                "word": word,
                "score": score
            }
            words.append(word)

        response = {"caption": caption, "words": words}

        return response
    except Exception as e :
        return {"Error":e}