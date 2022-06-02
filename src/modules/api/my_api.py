import uvicorn
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/hello")
def root():
    return {"message": "Hello World"}


@app.post("/upload_image")
async def upload_image(image: UploadFile = File(...)) -> UploadFile:
    return image


def run():
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
