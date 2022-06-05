from typing import Dict

import uvicorn
import aiofiles
import os
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

IMAGES_CAPTURED_PATH = "./images/"

app = FastAPI()

@app.post("/upload_image/{model}")
async def upload_image(model: str, image: UploadFile = File(...)) -> dict[str, str]:
    print(model)
    if not os.path.exists(IMAGES_CAPTURED_PATH):
        os.mkdir(IMAGES_CAPTURED_PATH)

    image_name = IMAGES_CAPTURED_PATH + image.filename

    async with aiofiles.open(image_name, 'wb') as out_file:
        while content := await image.read(1024):
            await out_file.write(content)

    return {'image': image.filename}


def run_api_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)


if __name__ == "__main__":
    run_api_server()
