from pydantic import BaseModel
from enum import Enum


class CategoryType(str, Enum):
    income = "income"
    expense = "expense"


class CategoryCreateRequest(BaseModel):
    name: str
    type: CategoryType


class CategoryPatchRequest(BaseModel):
    name: str | None = None
    type: CategoryType | None = None


class CategoryResponse(BaseModel):
    id: int
    user_id: int
    name: str
    type: str


class CategoryCreateResponse(BaseModel):
    message: str = "Category created successfully"
    created_item: CategoryResponse
