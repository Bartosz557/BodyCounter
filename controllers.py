import os

from PIL import Image

from fastapi import APIRouter
from markdown_it.rules_inline import image
from numpy.f2py.auxfuncs import throw_error

from webservices import analyze

router = APIRouter()


def get_name_for_id(image_id: int):
    valid_extensions = ('.jpg', '.jpeg')
    try:
        files = sorted(os.listdir('./resources'))
        image_files = [file for file in files if file.lower().endswith(valid_extensions)]
        if image_id < 1 or image_id > len(image_files):
            raise ValueError("Provided ID is out of bounds")
        return image_files[image_id - 1]
    except Exception as e:
        return f"An error occurred: {e}"


@router.get("/analyze-image/local")
def get_locale_image(image_id):
    if image_id.isnumeric():
        analyze(get_name_for_id(int(image_id)))
    else:
        analyze(image_id)


@router.get("/hello")
def get_users():
    return "hello"