from http import HTTPStatus

from facade_common.enums import FileEndpoints, RootEndpoints
from facade_common.logging import init_py_logger, logger
from facade_common.models import (
    InvocationPayloadModel,
    LambdaResponseHeadersModel,
    LambdaResponseModel,
)

from processors.files import process_file_request
from processors.root import process_index_request

init_py_logger()


def handler(event, _context):
    event_payload: InvocationPayloadModel = InvocationPayloadModel(**event)

    endpoint: str = event_payload.endpoint
    body: str = event_payload.body

    lambda_response_headers: LambdaResponseHeadersModel = LambdaResponseHeadersModel()
    lambda_response: LambdaResponseModel = LambdaResponseModel(
        is_base_64_encoded=False, status_code=HTTPStatus.OK, headers=lambda_response_headers.model_dump(by_alias=True)
    )

    if endpoint in RootEndpoints.values():
        lambda_response: LambdaResponseModel = process_index_request(endpoint=endpoint)

    if endpoint in FileEndpoints.values():
        lambda_response: LambdaResponseModel = process_file_request(endpoint=endpoint, body=body)

    return lambda_response.model_dump(by_alias=True)
