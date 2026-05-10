from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def build_success_payload(data=None, message="Success", code=status.HTTP_200_OK, metadata=None):
    payload = {
        "code": code,
        "status": "success",
        "message": message,
        "data": data if data is not None else {},
    }
    if metadata is not None:
        payload["metadata"] = metadata
    return payload


def build_error_payload(message="Error", error=None, code=status.HTTP_400_BAD_REQUEST):
    payload = {
        "code": code,
        "status": "error",
        "message": message,
        "error": error if error is not None else {},
    }
    return payload


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return Response(
            build_error_payload(
                message=str(exc),
                error=None,
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    data = response.data
    message = "An error occurred"
    error = data

    if isinstance(data, dict):
        detail = data.get("detail")
        if detail is not None:
            message = str(detail)
            error = detail
        else:
            message = "Validation error" if response.status_code == status.HTTP_400_BAD_REQUEST else str(data)
            error = data
    else:
        message = str(data)
        error = data

    return Response(build_error_payload(message=message, error=error, code=response.status_code), status=response.status_code)
