from datetime import timedelta

from miniopy_async import Minio


class Storage:
    def __init__(self, settings):
        self._bucket_name = settings.CV_BACKEND_MINIO_BUCKET_NAME
        self._client = Minio(
            endpoint=settings.CV_BACKEND_MINIO_ENDPOINT,
            access_key=settings.CV_BACKEND_MINIO_ACCESS_KEY,
            secret_key=settings.CV_BACKEND_MINIO_SECRET_KEY,
            secure=False,  # http for False, https for True
        )

    async def presigned_get_object(self, object_name: str) -> str:
        expires: timedelta = timedelta(hours=1)
        url = await self._client.presigned_get_object(
            bucket_name=self._bucket_name, object_name=object_name, expires=expires
        )
        return url

    async def presigned_put_object(self, object_name: str) -> str:
        expires: timedelta = timedelta(days=7)
        url = await self._client.presigned_put_object(
            bucket_name=self._bucket_name, object_name=object_name, expires=expires
        )
        return url
