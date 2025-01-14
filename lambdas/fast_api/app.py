import base64
import json
from contextlib import asynccontextmanager

from facade_common.enums import FileEndpoints, RootEndpoints
from facade_common.logging import init_py_logger
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from mangum import Mangum

from utils.file_request_processor import process_file_request
from utils.root_request_processor import process_root_request


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_py_logger()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/index")
async def index():
    return process_root_request(endpoint=str(RootEndpoints.INDEX))


@app.post("/upload")
async def upload_file(request: Request):
    form_data = await request.form()

    file = form_data.get("file")
    file_content = await file.read()

    body = {
        "name": file.filename,
        "content": base64.b64encode(file_content).decode("utf-8"),
        "content_type": file.content_type,
    }

    return process_file_request(endpoint=str(FileEndpoints.UPLOAD), body=body)


@app.post("/download")
async def download_file(request: Request):
    form_data = await request.form()

    bucket = form_data.get("bucket")
    file_key = form_data.get("file_key")

    body = {"bucket": bucket, "file_key": file_key}

    response = process_file_request(endpoint=str(FileEndpoints.DOWNLOAD), body=body)

    return StreamingResponse(**response)


def handler(event, context):
    app_handler = Mangum(app=app)
    return app_handler(event=event, context=context)
