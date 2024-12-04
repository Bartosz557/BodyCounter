from fastapi import APIRouter, UploadFile
from fastapi.params import File
from queue_services import add_task_to_queue
from webservices import save_image_from_url, check_job_status, save_image_from_user, get_name_for_id, validate_image

router = APIRouter()


@router.get("/analyze-image/local", description="Provide the ID or a name of the image to analyze.\nAvailable image options:\n1. cameleon\n2. cctv\n3. hill\n4. street\n5. suits\n6. walker")
def get_local_image(image_id):
    if image_id.isnumeric():
        return add_task_to_queue('./resources/' + get_name_for_id(int(image_id)))
    else:
        return add_task_to_queue('./resources/' + validate_image(image_id))


@router.get("/analyze-image/url")
def get_image_from_url(url):
    filename = save_image_from_url(url)
    return add_task_to_queue(filename)


@router.post("/upload/", description="Files required in format .jpg or .jpeg!")
async def upload_file(file: UploadFile = File(...)):
    filename = await save_image_from_user(file)
    return add_task_to_queue(filename)


@router.get("/check-job-status", description="Provide the ID or an Image Processing Job")
def get_job_status(job_id):
    return check_job_status(job_id)