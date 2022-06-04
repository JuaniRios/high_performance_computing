import asyncio
import datetime
import json
import os
import pickle
from typing import Literal, Optional
from asyncio import Queue, QueueEmpty
import logging
import requests
import uvicorn

from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse

from config import max_queue_size
from backup import backup_to_pickle

logging.basicConfig(level=logging.INFO, filename="history.log", encoding="utf-8")


class Job(BaseModel):
    owner: str
    url: str
    timestamp: datetime.datetime
    status: Literal[1, 2, 3]
    date_range: datetime.date
    assets: str


class Result(BaseModel):
    job: str  # assuming uri instead of pk
    timestamp: datetime.datetime
    assets: str
    weights: str


class QueueInfo(BaseModel):
    name: str


app = FastAPI()

if os.path.exists("queue_backup.pkl"):
    with open("queue_backup.pkl", "rb") as f:
        queues = pickle.load(f)
else:
    queues = {"jobs": Queue(maxsize=max_queue_size), "results": Queue(maxsize=max_queue_size)}


@app.middleware("http")
async def authentication(request: Request, call_next):
    # no auth on docs
    exempted_urls = [
        "http://localhost:7500/docs",
        "http://localhost:7500/redoc",
        "http://localhost:7500/openapi.json"
    ]
    if request.url in exempted_urls:
        response = await call_next(request)
        return response

    authorization = request.headers.get("authorization")
    if not authorization:
        return JSONResponse({"message": "no token provided"}, status_code=400)

    token = authorization[7:]
    auth_response = requests.post("http://localhost:8000/token", data={"token": token})

    if not auth_response.ok:
        return JSONResponse({"message": "invalid token"}, status_code=403)

    user_data = auth_response.json()
    request.state.user = user_data

    response = await call_next(request)
    return response


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    source = list(request.client)
    source = source[0] + ":" + str(source[1])
    destination = str(request.url)
    headers = dict(request.headers.items())
    # body = await request.json()

    data = json.dumps({
        "source": source,
        "destination": destination,
        "headers": headers,
        # "body": body,
        "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    logging.info(data)

    response = await call_next(request)
    return response


@app.on_event("startup")
async def backup():
    asyncio.create_task(backup_to_pickle(queues))

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/queues/{q_name}")
async def pull(q_name: str, request: Request):
    if hasattr(request.state, "user") and request.state.user["role"] not in ["ADMINISTRATOR", "MANAGER"]:
        raise HTTPException(status_code=403, detail="Only Admins and Managers can access this")

    if q_name not in queues:
        raise HTTPException(status_code=404, detail="Queue name not found")

    q = queues[q_name]
    item = await q.get()

    return {"response": item}


@app.post("/queues/{q_name}")
async def push(q_name: str, msg: Job | Result, request: Request):
    if hasattr(request.state, "user") and request.state.user["role"] not in ["ADMINISTRATOR", "MANAGER"]:
        raise HTTPException(status_code=403, detail="Only Admins and Managers can access this")

    if q_name not in queues:
        raise HTTPException(status_code=404, detail="Queue name not found")

    q = queues[q_name]

    await q.put(msg)

    return {"response": "push successful"}


@app.delete("/queues/{q_name}")
async def delete(q_name: str, request: Request):
    if hasattr(request.state, "user") and request.state.user["role"] != "ADMINISTRATOR":
        raise HTTPException(403, detail="Only Administrators can access this")

    try:
        del queues[q_name]
        return {"response": "success!"}
    except Exception as E:
        raise HTTPException(status_code=400, detail=E)


@app.get("/queues")
async def list_all(request: Request):
    if hasattr(request.state, "user") and request.state.user["role"] not in ["ADMINISTRATOR", "MANAGER"]:
        raise HTTPException(status_code=403, detail="Only Admins and Managers can access this")

    return {"response": list(queues.keys())}


@app.post("/queues")
async def create(q_info: QueueInfo, request: Request):
    if hasattr(request.state, "user") and request.state.user["role"] != "ADMINISTRATOR":
        raise HTTPException(status_code=403, detail="Only Admins and Managers can access this")

    if q_info.name in queues:
        raise HTTPException(400, detail="queue with that name already exists")

    try:
        queues[q_info.name] = Queue(maxsize=max_queue_size)
        return {"response": "success!"}

    except Exception as E:
        raise HTTPException(400, detail=E)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7500)

