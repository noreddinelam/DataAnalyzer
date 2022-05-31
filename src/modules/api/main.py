import uvicorn
from typing import Optional
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.get("/hello")
def root():
    return {"message": "Hello World"}

@app.post("/upload_image")
async def upload_image(image: UploadFile = File(...)):

    return {"filename": image.filename}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)