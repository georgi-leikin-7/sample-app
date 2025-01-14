from contextlib import asynccontextmanager

from facade_common.enums import FileEndpoints, RootEndpoints
from facade_common.logging import init_py_logger
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
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
    return process_file_request(endpoint=str(FileEndpoints.UPLOAD))


@app.get("/download")
async def download_file(request: Request):
    return process_file_request(endpoint=str(FileEndpoints.DOWNLOAD))


def handler(event, context):
    app_handler = Mangum(app=app)
    return app_handler(event=event, context=context)
