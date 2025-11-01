from pydantic import BaseModel
from datetime import datetime

class IncomeCreate(BaseModel):
    amount: float
    category: str
    description: str

class IncomeResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: str
    date_time: datetime

class IncomeCreateResponse(BaseModel):
    # message default value only can be overwrite
    message: str = "Income created successfully"
    income: IncomeResponse

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: str

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: str
    date_time: datetime

class ExpenseCreateResponse(BaseModel):
    message: str = "Expense created successfully"
    expense: ExpenseResponse