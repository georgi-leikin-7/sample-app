from facade_common.enums import EndpointEnum
from facade_common.logging import init_py_logger, logger
from facade_common.models import (
    InvocationPayloadModel,
    LambdaResponseModel,
    LambdaResponsePayloadModel,
)

init_py_logger()


def handler(event, _context):
    event_payload: InvocationPayloadModel = InvocationPayloadModel(**event)

    match event_payload.endpoint:
        case str(EndpointEnum.INDEX):
            logger.info(f"Processing request from the FastAPI /{event_payload.endpoint}.")

    response_payload = LambdaResponsePayloadModel(message=event_payload.endpoint)
    response = LambdaResponseModel(
        is_base_64_encoded=False,
        status_code=200,
        headers={"LambdaHeader": "Success!"},
        body=response_payload.model_dump_json(),
    )

    return response.model_dump(by_alias=True)
