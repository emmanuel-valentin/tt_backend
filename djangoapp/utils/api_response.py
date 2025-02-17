from rest_framework.response import Response
from rest_framework import status

def response_api(status="success", status_code=status.HTTP_200_OK, data=None, error=None, **kwargs):
    response = {
        "status": status,
        "statusCode": status_code,
        "data": data if data is not None else {},
        "error": error
    }
    response.update(kwargs)  # Permite agregar más datos adicionales
    return Response(response, status=status_code)
