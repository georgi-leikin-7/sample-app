from facade_common.enums import FileEndpoints


def process_file_request(endpoint: str):
    response = {}

    match endpoint:
        case str(FileEndpoints.UPLOAD):
            response = {"operation": "Upload"}

        case str(FileEndpoints.DOWNLOAD):
            response = {"operation": "Download"}

    return response
