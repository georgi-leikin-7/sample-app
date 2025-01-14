import json
from http import HTTPStatus

from facade_common.models import LambdaResponseHeadersModel, LambdaResponseModel


def process_index_request(endpoint: str) -> LambdaResponseModel:
    lambda_response_headers: LambdaResponseHeadersModel = LambdaResponseHeadersModel(content_type="application/json")
    return LambdaResponseModel(
        is_base_64_encoded=False,
        status_code=HTTPStatus.OK,
        headers=lambda_response_headers.model_dump(by_alias=True),
        body=json.dumps({"location": endpoint}),
    )
