import logging

import minio
from minio import Minio
from django.conf import settings
from urllib3 import BaseHTTPResponse


def get_object(document_name) -> BaseHTTPResponse:
    client = Minio(settings.MINIO_ADDRESS,
                   access_key=settings.MINIO_ACCESS_KEY,
                   secret_key=settings.MINIO_SECRET_KEY,
                   secure=False
                   )

    response, document = None, None
    try:
        response = client.get_object(settings.MINIO_BUCKET_NAME, document_name)
    except minio.S3Error as e:
        logging.error(e)
        raise e
    finally:
        if response:
            response.close()
            response.release_conn()

    return response
