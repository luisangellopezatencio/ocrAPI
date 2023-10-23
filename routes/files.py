from fastapi import APIRouter, UploadFile, File
from easyocr import Reader
from pydantic import BaseModel

class Item(BaseModel):
    url: str
    language: str = "es"



import requests

def get_image_from_url(url):
    """Descargar una imagen de una URL y devolverla como un objeto numpy.ndarray."""

    resp = requests.get(url, stream=True).raw
    image_bytes = resp.read()

    # Devolver la imagen.
    return image_bytes

route_files = APIRouter()

@route_files.post("/upload/file")
async def upload_file(file: UploadFile = File(...), language: str = "es"):
    """Subir un archivo y extraer el texto utilizando EasyOCR."""

    # Crear un lector de OCR.
    text_reader = Reader([language])

    # Leer el texto de la imagen.
    results = text_reader.readtext(file.file.read())

    # Extraer el texto reconocido con una probabilidad superior a 0,4.
    text_readed = []
    for (bbox, text, prob) in results:
        if prob > 0.4:
            text_readed.append(text)

    # Devolver el texto reconocido.
    if text_readed != []:
        return {"text_readed": text_readed}
    else:
        return {
            "success": True,
            "text_readed": [],
            "language": language,
            "message": "I can't read the text in the image :(, the image quality is too low."
        }

@route_files.post("/upload/url")
async def upload_url(item: Item):
    """Subir una imagen desde una URL y extraer el texto utilizando EasyOCR."""

    # Crear un lector de OCR.
    text_reader = Reader([item.language])

    # Leer la imagen de la URL.
    image = get_image_from_url(item.url)

    results = text_reader.readtext(image)

    # Extraer el texto reconocido con una probabilidad superior a 0,4.
    text_readed = []
    for (bbox, text, prob) in results:
        if prob > 0.4:
            text_readed.append(text)

# Devolver el texto reconocido.
    if text_readed != []:
        return {"text_readed": text_readed}
    else:
        return {
            "success": True,
            "text_readed": [],
            "language": item.language,
            "message": "I can't read the text in the image :(, the image quality is too low."
        }