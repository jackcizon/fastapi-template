from math import ceil

from src.core.dto.pagination import PaginationSchema, Pagination


class OffsetPaginator:
    def __init__(self, total: int, page_size: int, page: int) -> None:
        """
        Offset pagination is simple, widely used, and ideal for stable datasets like articles,
        admin panels, and searchable lists where page numbers and total counts matter.

        sql page query:

        - total: count(*) from `table`
        - limit = page_size
        - offset = (page - 1) * page_size

        A offset paginator needs 3 arguments: total, page_size, page.

        example:
        ```python
        class _TagInfo(TypedDict):
            id: int
            name: str


        class _TagInfoSchema(BaseModel):
            id: int
            name: str


        class UserTagsResponse(Pagination):
            # pagination: Pagination
            items: list[_TagInfo]


        class UserTagsResponseSchema(PaginationSchema):
            # pagination: PaginationSchema
            items: list[_TagInfoSchema]

        async def get_user_tags(self, user: User, *, offset: int, limit: int) -> UserTagsResponse:
            stat = (
                select(self.tag.id, self.tag.name)
                .where(self.tag.user_id == user.id)
                .offset(offset)
                .limit(limit)
            )
            res = await self.db.execute(stat)
            return cast(UserTagsResponse, res.mappings().all())

        async def get_user_all(username: str, db: AsyncSession, page: int, page_size: int) -> UserTagsResponse:
            user = await UserRepo(db).get_one_by_field_eq("name", username)
            if user is None:
                raise NotFoundError("User not exists.")

            total = await TagRepo(db).count()
            paginator = BasicPaginator(total=total, page=page, page_size=page_size)
            tags = await BlogRepo(db).get_user_tags(user, offset=paginator.offset, limit=paginator.limit)
            return UserTagsResponse(
                items=cast(list[dict[Any, Any]], tags),
                **paginator.paginate()
            )
        ```
        """

        self.total = total
        self.page_size = page_size
        self.page = page
        self.pages = max(1, ceil(total / page_size))

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    @property
    def next_page(self) -> int | None:
        return self.page + 1 if self.has_next else None

    @property
    def prev_page(self) -> int | None:
        return self.page - 1 if self.has_prev else None

    def paginate(self) -> Pagination:
        data = Pagination(
            page=self.page,
            page_size=self.page_size,
            pages=self.pages,
            total=self.total,
            has_next=self.has_next,
            has_prev=self.has_prev,
            next_page=self.next_page,
            prev_page=self.prev_page,
        )
        return PaginationSchema(**data).model_dump()
