import base64
import json
from io import BytesIO

import boto3
from facade_common.logging import logger
from facade_common.models import (
    InvocationPayloadModel,
    InvocationRequestModel,
    LambdaResponseModel,
)


def process_file_request(endpoint: str, body: dict | None = None) -> dict:
    logger.info(f"Processing request for '/{endpoint}' endpoint.")

    client = boto3.client("lambda")

    payload: InvocationPayloadModel = InvocationPayloadModel(endpoint=endpoint)

    if body:
        payload.body = json.dumps(body)

    request: InvocationRequestModel = InvocationRequestModel(
        function_name="fast-api-processor",
        invocation_type="requestResponse",
        payload=payload.model_dump_json(),
    )

    response = client.invoke(**request.model_dump(by_alias=True))

    response_payload = response.get("Payload").read().decode("utf-8")
    response_payload_dict: dict = json.loads(response_payload)

    response_model: LambdaResponseModel = LambdaResponseModel(**response_payload_dict)

    response_headers: dict = response_payload_dict.get("headers")

    response_body: str = response_model.body
    response_body_dict: dict = json.loads(response_body)

    if response_model.is_base_64_encoded:
        content = response_body_dict.get("content")
        medis_type = response_body_dict.get("media_type")

        file_content = base64.b64decode(content)
        content = BytesIO(file_content)

        return {"content": content, "media_type": medis_type, "headers": response_headers}

    return response_body_dict
