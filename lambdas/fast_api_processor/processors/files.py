import base64
import json
import mimetypes
from http import HTTPStatus

import boto3
from facade_common.enums import FileEndpoints
from facade_common.models import LambdaResponseHeadersModel, LambdaResponseModel


def process_file_request(endpoint: str, body: str | None = None) -> LambdaResponseModel:

    lambda_response_headers: LambdaResponseHeadersModel = LambdaResponseHeadersModel()
    lambda_response: LambdaResponseModel = LambdaResponseModel(
        is_base_64_encoded=False,
        status_code=HTTPStatus.OK,
        headers=lambda_response_headers.model_dump(by_alias=True, mode="json"),
    )

    client = boto3.client("s3")

    match endpoint:
        case str(FileEndpoints.UPLOAD):
            json_body: dict = json.loads(body)

            file_name = json_body.get("name")

            encoded_file_content: str = json_body.get("content")
            file_content: bytes = base64.b64decode(encoded_file_content)

            content_type = json_body.get("content_type")

            client.put_object(
                Bucket="facade.files", Key=f"pdf/{file_name}", Body=file_content, ContentType=content_type
            )

            lambda_response.body = json.dumps({"message": f"File {file_name} upload"})

        case str(FileEndpoints.DOWNLOAD):
            json_body: dict = json.loads(body)

            bucket = json_body.get("bucket")
            file_key = json_body.get("file_key")

            media_type, _ = mimetypes.guess_type(file_key)
            if not media_type:
                media_type = "application/octet-stream"

            s3_response = client.get_object(Bucket=bucket, Key=f"pdf/{file_key}")

            file_content: bytes = s3_response.get("Body").read()
            encoded_file_content: str = base64.b64encode(file_content).decode("utf-8")
            content_type = s3_response.get("ContentType")

            lambda_response_headers.content_type = content_type
            lambda_response_headers.content_disposition = f"attachment; filename={file_key}"

            lambda_response.is_base_64_encoded = True
            lambda_response.headers = lambda_response_headers.model_dump(by_alias=True, mode="json")
            lambda_response.body = json.dumps(
                {"file_key": file_key, "content": encoded_file_content, "media_type": media_type}
            )

    return lambda_response
