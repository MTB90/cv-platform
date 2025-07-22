from miniopy_async import Minio


class Storage:
    def __init__(self, settings):
        self._client = Minio(
            endpoint=settings.CV_BACKEND_MINIO_ENDPOINT,
            access_key=settings.CV_BACKEND_MINIO_ACCESS_KEY,
            secret_key=settings.CV_BACKEND_MINIO_SECRET_KEY,
            secure=False,  # http for False, https for True
        )

    async def presigned_get_object(self) -> str:
        pass

    async def presigned_put_object(self) -> str:
        pass
