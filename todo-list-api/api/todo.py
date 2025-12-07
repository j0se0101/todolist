import os
import time
import boto3
from typing import Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel
from boto3.dynamodb.conditions import Key

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(app)


class PutTaskRequest(BaseModel):
    content: str
    user_id: str  # Hacerlo obligatorio
    task_id: Optional[str] = None
    is_done: bool = False


@app.get("/")
async def root():
    return {"message": "Hello from ToDo API!"}


@app.put("/create-task")
async def create_task(put_task_request: PutTaskRequest):
    if not put_task_request.user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    
    created_time = int(time.time())
    task_id = f"task_{uuid4().hex}"
    item = {
        "user_id": put_task_request.user_id,
        "task_id": task_id,
        "content": put_task_request.content,
        "is_done": False,
        "created_time": created_time,
        "ttl": int(created_time + 86400),
    }

    table = _get_table()
    table.put_item(Item=item)
    return {"task": item}


@app.get("/get-task/{user_id}/{task_id}")
async def get_task(user_id: str, task_id: str):
    table = _get_table()
    response = table.get_item(Key={"user_id": user_id, "task_id": task_id})
    item = response.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return item


@app.get("/list-tasks/{user_id}")
async def list_tasks(user_id: str):
    # List the top N tasks from the table, using the user index.
    table = _get_table()
    response = table.query(
        IndexName="user-index",
        KeyConditionExpression=Key("user_id").eq(user_id),
        ScanIndexForward=False,
        Limit=10,
    )
    tasks = response.get("Items")
    return {"tasks": tasks}


@app.put("/update-task")
async def update_task(put_task_request: PutTaskRequest):
    if not put_task_request.user_id or not put_task_request.task_id:
        raise HTTPException(status_code=400, detail="user_id and task_id are required")
    
    table = _get_table()
    table.update_item(
        Key={"user_id": put_task_request.user_id, "task_id": put_task_request.task_id},
        UpdateExpression="SET content = :content, is_done = :is_done",
        ExpressionAttributeValues={
            ":content": put_task_request.content,
            ":is_done": put_task_request.is_done,
        },
        ReturnValues="ALL_NEW",
    )
    return {"updated_task_id": put_task_request.task_id}


@app.delete("/delete-task/{user_id}/{task_id}")
async def delete_task(user_id: str, task_id: str):
    table = _get_table()
    table.delete_item(Key={"user_id": user_id, "task_id": task_id})
    return {"deleted_task_id": task_id}


def _get_table():
    table_name = os.environ.get("TABLE_NAME")
    return boto3.resource("dynamodb").Table(table_name)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
