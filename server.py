import cv2 
import io
import os
import uvicorn
import numpy as np
from enum import Enum
import nest_asyncio
from fastapi import FastAPI, UploadFile, File , HTTPException
from fastapi.responses import StreamingResponse
import torch

app = FastAPI(title="Deploying a Computer vision Model")

# class Model(str, Enum):
#     yolov5 = "ultralytics/yolov5"
#     yolov3 = "yolov3"

@app.get("/")
def home():
    return "Your API is working fine. Head over to http://localhost:8000/docs to access the client side of this api and feel free to test this API."



@app.post("/predict")
def prediction( file: UploadFile = File(...)):
    filename = file.filename
    fileExtention = filename.split(".")[-1] in ("jpg","jpeg","png")
    if not fileExtention:
        raise HTTPException(status_code=415, detail="Unsupported file provided")

    
    image_stream = io.BytesIO(file.file.read())

    image_stream.seek(0)

    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)

    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    model = torch.hub.load("ultralytics/yolov5","custom",'best.pt')

    result = model(image)

    result.save()
    
    dir = sorted(os.listdir("runs/detect")[3:])[-1]

    print("reading image"+f'runs/detect/{dir}/image0.jpg')

    file_image = open(f'runs/detect/{dir}/image0.jpg',mode="rb")

    return StreamingResponse(file_image, media_type="image/jpeg")

nest_asyncio.apply()

host = "0.0.0.0" #if os.getenv("DOCKER-SETUP") else "127.0.0.1"

# uvicorn.run(app, host=host, port=8000)

