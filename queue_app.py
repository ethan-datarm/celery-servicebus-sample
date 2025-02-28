from celery import Celery
import time
import os

# Service Bus Connection Details for Queue
SERVICE_BUS_KEY_NAME = os.getenv("SERVICE_BUS_KEY_NAME")
SERVICE_BUS_KEY = os.getenv("SERVICE_BUS_KEY")
SERVICE_BUS_NAMESPACE = "my_servicebus_name"
SERVICE_BUS_QUEUE_NAME = "my_queue_name"

# Azure Blob Connection Details for Status Storage
AZURE_BLOB_CONNECTION_STRING = os.getenv("AZURE_BLOB_CONNECTION_STRING")

# Azure Blob Connection Details
# default container name must exist, "celery"
AZURE_BLOB_CONNECTION_STRING = os.getenv("AZURE_BLOB_CONNECTION_STRING")

celery_app = Celery(
    "my_app",
    broker_url=f"azureservicebus://{SERVICE_BUS_KEY_NAME}:{SERVICE_BUS_KEY}@{SERVICE_BUS_NAMESPACE}",
    backend=f"azureblockblob://{AZURE_BLOB_CONNECTION_STRING}"
)

@celery_app.task
def process_data(data):
    # Simulate delay
    time.sleep(2)
    
    # Simulate processing data
    return f"Processed data: {data}" 