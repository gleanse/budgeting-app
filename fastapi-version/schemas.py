from pydantic import BaseModel
from datetime import datetime

# INCOME
class IncomeCreate(BaseModel):
    amount: float
    category_id: int
    description: str

class IncomeResponse(BaseModel):
    id: int
    amount: float
    category_id: int
    category_name: str
    description: str
    date_time: datetime

class IncomeCreateResponse(BaseModel):
    # message default value only can be overwrite
    message: str = "Income created successfully"
    income: IncomeResponse


# EXPENSE
class ExpenseCreate(BaseModel):
    amount: float
    category_id: int
    description: str

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category_id: int
    category_name: str
    description: str
    date_time: datetime

class ExpenseCreateResponse(BaseModel):
    message: str = "Expense created successfully"
    expense: ExpenseResponse

# CATEGORY
class CategoryCreate(BaseModel):
    name: str
    type: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    type: str
    user_id: int

class CategoryCreateResponse(BaseModel):
    message: str = "Category created successfully"
    category: CategoryResponse