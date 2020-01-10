# fastapi
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

# Image
import base64
from PIL import Image
from io import BytesIO

# S3
import s3

# pydantic for Model
from pydantic import BaseModel
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'])


class Iresponse_photo(BaseModel):
    photo_data_uri: str
    file_name: str
    bucket_name: str


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


@app.get("/_api/photo", response_model=Iresponse_photo)
def get_photo(name: str, bucket: str="face-image"):
    file_path = "s3://"+bucket+"/"+name
    try:
        data_uri = image_to_data_uri(get_s3_image(file_path))
        return {
            "photo_data_uri": data_uri,
            "file_name": name,
            "bucket_name": bucket
        }
    except:
        raise HTTPException(status_code=404, detail="Photo " +
                            name + " not found in bucket "+bucket)
