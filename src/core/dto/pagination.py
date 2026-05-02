from typing import TypedDict

from pydantic import BaseModel


class Pagination(TypedDict):
    page: int
    page_size: int
    pages: int
    total: int
    has_prev: bool
    has_next: bool
    prev_page: int | None
    next_page: int | None


class PaginationSchema(BaseModel):
    page: int
    page_size: int
    pages: int
    total: int
    has_prev: bool
    has_next: bool
    prev_page: int | None
    next_page: int | None
