from pydantic import BaseModel
from datetime import datetime


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
    message: str = "Income created successfully"
    income: IncomeResponse

class IncomeDelete(BaseModel):
    id: int
    amount: float
    category_id: int

class IncomeDeleteResponse(BaseModel):
    message: str = "Income record deleted successfully"
    deleted_item: IncomeDelete