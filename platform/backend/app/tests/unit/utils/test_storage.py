import pytest

from utils.storage import MinioClient


@pytest.mark.anyio
async def test_given_mock_settings_when_create_minio_client_then_client_created(
    mock_settings,
):
    MinioClient(mock_settings)
