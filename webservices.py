import random
from fastapi import HTTPException
from rq import Queue
import io
import os
from PIL import Image
from redis import Redis
import requests


valid_extensions = ('.jpg', '.jpeg')


def save_image_from_url(image_url):
    save_path = './saved_images/' + generate_ID() + '.jpg'
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image successfully downloaded to {save_path}")
            return save_path
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")
            raise HTTPException(status_code=500,
                                detail=f"Failed to retrieve image. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid URL or network issue: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


async def save_image_from_user(file):
    if not (file.filename.lower().endswith(valid_extensions)):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .jpg image.")
    image_data = await file.read()
    save_path = './saved_images/' + file.filename

    try:
        image = Image.open(io.BytesIO(image_data))
        image.save(save_path)
        return save_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")


def check_job_status(job_id: str):
    redis_conn = Redis()
    q = Queue('task_queue',connection=redis_conn)
    job = q.fetch_job(job_id)
    print(f"Job ID: {job.id}")
    print(f"Job Status: {job._status}")
    print(f"Detected_Human: {job.meta}")
    return {
        "Job_ID": job.id,
        "job_id": job._status,
        "Detected_Human": job.meta
    }



## HELPERS

def get_name_for_id(image_id: int):
    try:
        files = sorted(os.listdir('./resources'))
        image_files = [file for file in files if file.lower().endswith(valid_extensions)]
        if image_id < 1 or image_id > len(image_files):
            raise HTTPException(status_code=404, detail="Image not found. Index out of bounds")
        return image_files[image_id - 1]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def validate_image(image_id):
    image = image_id + '.jpg' if not image_id.lower().endswith(valid_extensions) else image_id
    if os.path.exists('./resources/' + image):
        return image
    raise HTTPException(status_code=404, detail=f"File '{image_id}' not found in the local resources")


def generate_ID():
    return str(random.randint(100000, 999999))


def clear_saved_images():
    directory ='./saved_images'
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
    print("...Saved images removed")

