from contextvars import ContextVar
from typing import Optional

request_id: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


def get_request_id() -> str:
    return request_id.get(None) or ""


def set_request_id(request_id_to_set: str) -> None:
    request_id.set(request_id_to_set)
