from fastapi import FastAPI
from celery.result import AsyncResult
from queue_app import celery_app, process_data
from datetime import datetime
app = FastAPI()

@app.get("/")
async def hello_world():
    return {"message": f"Hello World at {datetime.now()}"} 

@app.post("/enqueue/")
async def enqueue_data(data: dict):
    # Will enqueue the data to the service bus queue from JSON object in the request body
    # Returns the task id to check for status
    task = process_data.delay(data)
    return {"task_id": task.id}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    # Returns the status of the task
    task_result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "status": task_result.status, "result": task_result.result} 
