from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class IncomeCreateRequest(BaseModel):
    amount: Decimal
    category_id: int | None = None
    account_id: int
    description: str | None = None
    date_time: datetime | None = None


class IncomePatchRequest(BaseModel):
    amount: Decimal | None = None
    category_id: int | None = None
    account_id: int | None = None
    description: str | None = None
    date_time: datetime | None = None


class IncomeListResponse(BaseModel):
    id: int
    amount: Decimal
    category_name: str
    account_name: str
    date_time: datetime


class IncomeDetailResponse(BaseModel):
    id: int
    amount: Decimal
    category_id: int | None
    category_name: str
    account_id: int
    account_name: str
    description: str | None
    date_time: datetime


class IncomeCreateResponse(BaseModel):
    message: str = "Income created successfully"
    created_item: IncomeDetailResponse
