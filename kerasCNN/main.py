from fastapi import FastAPI, UploadFile, File
import uvicorn
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
from io import BytesIO
from PIL import Image

app = FastAPI()
model = load_model("cat_dog_model.h5")
# Add this to your main.py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict/upload")
async def predict_upload(file: UploadFile = File(...)):
    # Read image file as bytes
    contents = await file.read()
    img = Image.open(BytesIO(contents)).convert("RGB")
    img = img.resize((150, 150))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.0
    prediction = model.predict(img_tensor)
    result = "Dog" if prediction[0][0] > 0.5 else "Cat"
    return {"filename": file.filename, "prediction": result}

@app.get("/predict/{image_name}")
def predict_image(image_name: str):
    img_path = f"data/{image_name}"
    img = image.load_img(img_path, target_size=(150, 150))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.0
    prediction = model.predict(img_tensor)
    result = "Dog" if prediction[0][0] > 0.5 else "Cat"
    return {"image_name": image_name, "prediction": result}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)