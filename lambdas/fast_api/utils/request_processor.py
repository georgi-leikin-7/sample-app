import json

import boto3
from facade_common.logging import logger
from facade_common.models import (
    InvocationPayloadModel,
    InvocationRequestModel,
    LambdaResponseModel,
    LambdaResponsePayloadModel,
)


def process_request(endpoint: str) -> LambdaResponsePayloadModel:
    logger.info(f"Processing request for '/{endpoint}' endpoint.")

    client = boto3.client("lambda")

    payload: InvocationPayloadModel = InvocationPayloadModel(endpoint=endpoint)
    request: InvocationRequestModel = InvocationRequestModel(
        function_name="fast-api-processor",
        invocation_type="requestResponse",
        payload=payload.model_dump_json(),
    )

    response = client.invoke(**request.model_dump(by_alias=True))

    response_payload = response.get("Payload").read().decode("utf-8")
    response_payload_dict: dict = json.loads(response_payload)

    response_model: LambdaResponseModel = LambdaResponseModel(**response_payload_dict)

    response_body: str = response_model.body
    response_body_dict: dict = json.loads(response_body)
    response_body_model: LambdaResponsePayloadModel = LambdaResponsePayloadModel(**response_body_dict)

    return response_body_model
