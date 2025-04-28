from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        logger.error(f"Unhandled error: {str(exc)}")
        response = Response({
            "error": "An unexpected error occurred",
            "detail": str(exc) if not None else "Unknown error"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        logger.error(f"API error: {str(exc)}")

    # Add request info to response
    request = context.get('request')
    if request:
        response.data['path'] = request.path
        response.data['method'] = request.method

    return response