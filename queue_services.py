import cv2
from redis import Redis
from rq import Queue, get_current_job
from webservices import clear_saved_images


redis_conn = Redis(host="localhost", port=6379)
task_queue = Queue("task_queue", connection=redis_conn)


def add_task_to_queue(filename: str):
    job_instance = task_queue.enqueue(process_task, filename)
    print(job_instance)
    print("task added to queue")
    return {
         "message": "Job has been enqueued",
         "job_id": job_instance.id
    }


def process_task(filename: str):
    print("processing task...")
    print("Path of the processed image: "+filename)
    image = cv2.imread(filename)

    job = get_current_job()
    job_id = job.id if job else None
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    (humans, _) = hog.detectMultiScale(image, winStride=(10, 10), padding=(32, 32), scale=1.1)

    job.meta = len(humans)
    job.save()
    print('Human Detected : ', len(humans))

    # Marking found humans on the image
    for (x, y, w, h) in humans:
        pad_w, pad_h = int(0.15 * w), int(0.01 * h)
        cv2.rectangle(image, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), 2)

    cv2.imwrite(f'./analyzed-images/{job_id}.jpg', image)
    clear_saved_images()



