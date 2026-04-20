from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class ExpenseCreateRequest(BaseModel):
    amount: Decimal
    category_id: int
    account_id: int
    description: str


class ExpensePatchRequest(BaseModel):
    amount: Decimal | None = None
    category_id: int | None = None
    account_id: int | None = None
    description: str | None = None


class ExpenseListResponse(BaseModel):
    id: int
    amount: Decimal
    category_name: str
    account_name: str
    date_time: datetime


class ExpenseDetailResponse(BaseModel):
    id: int
    amount: Decimal
    category_id: int
    category_name: str
    account_id: int
    account_name: str
    description: str
    date_time: datetime


class ExpenseCreateResponse(BaseModel):
    message: str = "Expense created successfully"
    created_item: ExpenseDetailResponse
