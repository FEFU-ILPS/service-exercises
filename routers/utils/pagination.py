from typing import Generic, TypeVar

from pydantic import BaseModel, Field, computed_field


M = TypeVar("M", bound=BaseModel)


class Pagination(BaseModel):
    page: int = Field(gt=0)
    size: int = Field(gt=0)

    @computed_field
    @property
    def skip(self) -> int:
        return (self.page - 1) * self.size


class PaginatedResponse(Generic[M], BaseModel):
    items: list[M]
    page: int
    size: int
    total: int

    @computed_field
    @property
    def total_pages(self) -> int:
        return (self.total + self.size - 1) // self.size
