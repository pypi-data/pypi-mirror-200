from logging import INFO, LogRecord
from typing import cast

import pytest

from sag_py_fastapi_request_id import RequestContextLoggingFilter, RequestIdLogRecord, request_context


@pytest.fixture()
def log_record() -> LogRecord:
    return LogRecord(name="", level=INFO, pathname="", lineno=0, msg="Hello, world!", args=(), exc_info=None)


def test_request_context_logging_filter_with_value(log_record: LogRecord) -> None:
    # Arrange
    request_context.set_request_id("ABC")
    filter_ = RequestContextLoggingFilter()

    # Act
    filter_.filter(log_record)

    # Assert
    assert cast(RequestIdLogRecord, log_record).request_id == "ABC"


def test_request_context_logging_filter_without_value(log_record: LogRecord) -> None:
    # Arrange
    request_context.set_request_id("")
    filter_ = RequestContextLoggingFilter()

    # Act
    filter_.filter(log_record)

    # Assert
    filter_.filter(log_record)
    assert not hasattr(log_record, "request_id")
