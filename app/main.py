# fastapi
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# Image
import base64
from PIL import Image
from io import BytesIO

# S3
import s3

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'])


def image_to_data_uri(img: Image.Image):
    buffered = BytesIO()
    img.save(buffered, 'JPEG')
    img_base64 = base64.b64encode(buffered.getvalue())
    data_uri_byte = bytes("data:image/jpeg;base64,",
                          encoding='utf-8') + img_base64
    data_uri_string = data_uri_byte.decode('utf-8')
    return data_uri_string


def get_s3_image(uri: str):
    img_stream = s3.get_file_stream(uri)
    return Image.open(img_stream)


@app.get("/_api/photo")
def get_photo(name: str, bucket: str="face-image"):
    file_path = "s3://"+bucket+"/"+name
    return {
        "image": image_to_data_uri(get_s3_image(file_path))
    }