# Queue Processing API

A simple FastAPI application that demonstrates asynchronous task processing using Celery.
Created for Clare demo app.

## Overview

This application provides a REST API for enqueueing data processing tasks and checking their status. It uses:

- **FastAPI**: A modern, fast web framework for building APIs
- **Celery**: Distributed task queue for processing background jobs
- **Azure Service Bus**: Message broker for storing and managing tasks queue (an alternative to Redis or RabbitMQ)
- **Azure Blob Storage**: Storage for task status & logs

## Installation

1. Clone this repository & set up Virtual Environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Azure Prerequisites

### Service Bus

- Create a Service Bus Instance (aka namespace)
- Create a queue within it
- Generate a connection string for the Service Bus - this will have a key name and key value, you'll need both

### Storage

- Create a Storage Account
- Create a Storage Container (default name is "celery")
- Generate a connection string for the Storage Account - either Admin Connection String or SAS for Blob Storage

## Environment Variables

Set Environment Variables for the Service Bus and Storage connection strings
- `SERVICE_BUS_KEY_NAME` - the key name from the Service Bus connection string (e.g. "RootManageSharedAccessKey")
- `SERVICE_BUS_KEY` - the key value from the Service Bus connection string (e.g. "xxx=")
- `AZURE_BLOB_CONNECTION_STRING` - the connection string for the Storage Account (e.g. "DefaultEndpointsProtocol=https;AccountName=my_storage_account;AccountKey=xxx;EndpointSuffix=core.windows.net")
- `SERVICE_BUS_NAMESPACE` - the namespace of the Service Bus (e.g. "my_servicebus_name")
- `SERVICE_BUS_QUEUE_NAME` - the name of the queue in the Service Bus (e.g. "my_queue_name")

A .env file is included in the repo for convenience, but other methods of setting environment variables are supported. Rename the .env.example file to .env and set the variables.

## Running the Application

1. Start the Celery worker in a Terminal window:

```bash
celery -A queue_app.celery_app worker --loglevel=info
```

2. Start the FastAPI application in another Terminal window:

```bash
uvicorn main:app --reload --port 8001
```

## API Endpoints

Default local host URI is http://127.0.0.1:8001

### POST /enqueue/

Enqueues data for processing. Accepts a arbitrarty JSON object in the request body. Service Bus limitation is 256KB per message.

**Request**:
```json
{
  "key1": "value1",
  "key2": "value2"
}
```

**Response**:
```json
{
  "task_id": "task-guid-string"
}
```

### GET /status/{task_id}

Checks the status of a task.

**Response**:
```json
{
  "task_id": "task-uuid-string",
  "status": "PENDING|STARTED|SUCCESS|FAILURE",
  "result": null|<task-result>
}
```

### GET /

Uptime health check. Returns a simple hello world message.

**Response**:
```json
{
  "message": "Hello World"
}
```
## License

MIT 