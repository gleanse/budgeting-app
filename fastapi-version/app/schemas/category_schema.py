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
