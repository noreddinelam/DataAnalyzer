from typing import Dict

import uvicorn
import aiofiles
import os
from src.data.data_processing import perfom_prediction
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload_image/{model}")
async def upload_image(model: str, image: UploadFile = File(...)) -> dict[str, str]:
    image_path = "../api/images_captured/"
    if not os.path.exists(image_path):
        os.mkdir(image_path)

    image_name = image_path + image.filename

    async with aiofiles.open(image_name, 'wb') as out_file:
        while content := await image.read(1024):
            await out_file.write(content)
    res = perfom_prediction(image_name, model)
    os.remove(image_name)
    return res


def run_api_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)


if __name__ == "__main__":
    run_api_server()
