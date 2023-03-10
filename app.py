import os
import numpy as np
import mlfoundry as mlf
from PIL import Image
from io import BytesIO
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse
from skimage.transform import resize
from fastapi import FastAPI

app = FastAPI()
model = mlf.get_client().get_model(os.getenv("MODEL_VERSION_FQN")).load()

def recognize_digit(image):
    image = image.reshape(1, 28, 28, 1)  # add a batch dimension
    prediction = model.predict(image).tolist()[0]
    return {str(i): prediction[i] for i in range(10)}

def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)))

@app.get("/", response_class=HTMLResponse)
def root():
    html_content = "<html><body>Open <a href='/docs'>Docs</a></body></html>"
    return HTMLResponse(content=html_content, status_code=200)

@app.post('/predict')
async def predict(image: UploadFile = File(...)):
    np_image = load_image_into_numpy_array(await image.read())
    return {'predictions': recognize_digit(resize(np_image, (28, 28, 1)))}