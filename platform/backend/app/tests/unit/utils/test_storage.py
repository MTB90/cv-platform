import pytest

from utils.storage import StorageClient


@pytest.mark.anyio
async def test_given_mock_settings_when_create_minio_client_then_client_created(
    mock_settings,
):
    StorageClient(mock_settings)
