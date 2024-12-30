from contextlib import asynccontextmanager

from facade_common.enums import EndpointEnum
from facade_common.logging import init_py_logger
from facade_common.models import LambdaResponsePayloadModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from utils.request_processor import process_request


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
    response: LambdaResponsePayloadModel = process_request(endpoint=str(EndpointEnum.INDEX))
    return {"message": f"Called `/{response.message}` endpoint."}


def handler(event, context):
    app_handler = Mangum(app=app)
    return app_handler(event=event, context=context)
