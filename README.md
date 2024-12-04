Start the application:
    
    fastapi dev main.py

For macOS - before starting workers, to fix the fork() problem with RQ multithreading


    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES


Start an RQ workers:

    rq worker task_queue


Swagger API documentation:

    http://localhost:8000/docs

