from pydantic import BaseModel
from decimal import Decimal


class BudgetCreateRequest(BaseModel):
    category_id: int
    limit_amount: Decimal
    month: int
    year: int


class BudgetPatchRequest(BaseModel):
    limit_amount: Decimal | None = None


class BudgetListResponse(BaseModel):
    id: int
    category_name: str
    limit_amount: Decimal
    spent_amount: Decimal
    remaining: Decimal


class BudgetDetailResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    category_name: str
    limit_amount: Decimal
    month: int
    year: int
    spent_amount: Decimal
    remaining: Decimal


class BudgetCreateResponse(BaseModel):
    message: str = "Budget created successfully"
    created_item: BudgetDetailResponse
