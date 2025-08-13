from uuid import UUID

import pytest

from app.schema.doc import DocStatus, DocEvent


@pytest.mark.parametrize(
    "event, key, expected",
    [
        pytest.param(
            "s3:ObjectCreated:Post",
            "bucket/17619270-9141-4b9d-ac97-c42584d12cbb/f5d3a088-3ca2-443e-930c-ac20adaf2fc6.pdf",
            {
                "user_id": UUID("17619270-9141-4b9d-ac97-c42584d12cbb"),
                "doc_id": UUID("f5d3a088-3ca2-443e-930c-ac20adaf2fc6"),
                "event_name": DocStatus.READY,
            },
            id="create",
        ),
        pytest.param(
            "s3:ObjectRemoved:Delete",
            "bucket/17619270-9141-4b9d-ac97-c42584d12cbb/f5d3a088-3ca2-443e-930c-ac20adaf2fc6.txt",
            {
                "user_id": UUID("17619270-9141-4b9d-ac97-c42584d12cbb"),
                "doc_id": UUID("f5d3a088-3ca2-443e-930c-ac20adaf2fc6"),
                "event_name": DocStatus.DELETED,
            },
            id="delete",
        ),
    ],
)
def test_doc_update_status_when_correct_values_no_exception(event, key, expected):
    try:
        DocEvent.model_validate({"EventName": event, "Key": key})
    except Exception as exc:
        pytest.fail(f"Unexpected exception: {exc}")


@pytest.mark.parametrize(
    "event, key",
    [
        pytest.param(
            "s3:ObjectCreated:Post",
            "17619270-9141-4b9d-ac97-c42584d12cbb/f5d3a088-3ca2-443e-930c-ac20adaf2fc6.pdf",
            id="missing bucket name",
        ),
        pytest.param(
            "s3:ObjectCreated:Invalid",
            "bucket/17619270-9141-4b9d-ac97-c42584d12cbb/f5d3a088-3ca2-443e-930c-ac20adaf2fc6.txt",
            id="invalid schema for event",
        ),
        pytest.param(
            "s3:ObjectRemoved:Delete",
            "bucket/17619270/ac20adaf2fc6.txt",
            id="invalid user id and doc id",
        ),
        pytest.param(
            "s3:ObjectRemoved:Delete",
            "bucket/17619270/ac20adaf2fc6.txt",
            id="invalid user id and doc id",
        ),
        pytest.param("s3:ObjectRemoved:Delete", None, id="missing key"),
    ],
)
def test_doc_update_status_when_invalid_values_raise_value_error(event, key):
    with pytest.raises(ValueError):
        DocEvent.model_validate({"EventName": event, "Key": key})
