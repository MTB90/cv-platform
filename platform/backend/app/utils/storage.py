import logging
from datetime import timedelta

from miniopy_async import Minio

from core.exceptions import StorageServiceError

logger = logging.getLogger(__name__)


class MinioClient:
    def __init__(self, settings):
        self._bucket_name = settings.CV_BACKEND_MINIO_BUCKET_NAME
        self._client = Minio(
            endpoint=settings.CV_BACKEND_MINIO_ENDPOINT,
            access_key=settings.CV_BACKEND_MINIO_ACCESS_KEY,
            secret_key=settings.CV_BACKEND_MINIO_SECRET_KEY,
            server_url=settings.CV_BACKEND_MINIO_SERVER_URL,
            secure=False,  # http for False, https for True
        )

    async def presigned_get_object(self, object_name: str) -> str:
        expires: timedelta = timedelta(hours=1)

        try:
            return await self._client.presigned_get_object(
                bucket_name=self._bucket_name, object_name=object_name, expires=expires
            )
        except Exception as e:
            logger.error("can't create presigned url for download", exc_info=e)
            raise StorageServiceError()

    async def presigned_put_object(self, object_name: str) -> str:
        expires: timedelta = timedelta(days=7)

        try:
            return await self._client.presigned_put_object(
                bucket_name=self._bucket_name, object_name=object_name, expires=expires
            )
        except Exception as e:
            logger.error("can't create presigned url for upload", exc_info=e)
            raise StorageServiceError()
