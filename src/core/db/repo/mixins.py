from typing import Any


class BatchCreateMixin:
    def batch_create(self, params: list[dict[str, Any]] = None) -> None:
        raise NotImplementedError
