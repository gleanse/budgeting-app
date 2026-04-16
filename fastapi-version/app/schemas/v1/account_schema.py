from pydantic import BaseModel


class AccountCreate(BaseModel):
    name: str


class AccountResponse(BaseModel):
    id: int
    name: str


class AccountBalanceResponse(BaseModel):
    total_balance: float
