from typing import Dict

import uvicorn
import aiofiles
import os
from fastapi import FastAPI, File, UploadFile

IMAGES_CAPTURED_PATH = "./images_captured"

app = FastAPI()


@app.get("/hello")
def root():
    return {"message": "Hello World"}


@app.post("/upload_image")
async def upload_image(image: UploadFile = File(...)) -> dict[str, str]:
    if not os.path.exists(IMAGES_CAPTURED_PATH):
        os.mkdir(IMAGES_CAPTURED_PATH)

    image_name = IMAGES_CAPTURED_PATH + "/" + image.filename

    async with aiofiles.open(image_name, 'wb') as out_file:
        content = await image.read()
        await out_file.write(content)

    return {"message": "OK"}


def run_api_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)


if __name__ == "__main__":
    run_api_server()
