from pydantic import BaseModel
from enum import Enum


class CategoryType(str, Enum):
    income = "income"
    expense = "expense"


class CategoryCreate(BaseModel):
    name: str
    type: CategoryType


class CategoryResponse(BaseModel):
    id: int
    name: str
    type: str
    user_id: int


class CategoryCreateResponse(BaseModel):
    message: str = "Category created successfully"
    category: CategoryResponse


class CategoryDelete(BaseModel):
    id: int
    name: str
    type: str


class CategoryDeleteResponse(BaseModel):
    message: str = "Category deleted successfully"
    deleted_item: CategoryDelete
