from pydantic import BaseModel
from datetime import datetime


class ExpenseCreate(BaseModel):
    amount: float
    category_id: int
    account_id: int
    description: str


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category_id: int
    category_name: str
    account_id: int
    account_name: str
    description: str
    date_time: datetime


class ExpenseCreateResponse(BaseModel):
    message: str = "Expense created successfully"
    expense: ExpenseResponse


class ExpenseDelete(BaseModel):
    id: int
    amount: float
    category_id: int


class ExpenseDeleteResponse(BaseModel):
    message: str = "Expense record deleted successfully"
    deleted_item: ExpenseDelete
