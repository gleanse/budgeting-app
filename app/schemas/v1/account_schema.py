from pydantic import BaseModel
from decimal import Decimal


class AccountCreateRequest(BaseModel):
    name: str
    initial_balance: Decimal


class AccountPatchRequest(BaseModel):
    name: str | None = None


class AccountResponse(BaseModel):
    id: int
    user_id: int
    name: str
    initial_balance: Decimal
    total_balance: Decimal


class AccountCreateResponse(BaseModel):
    message: str = "Account created successfully"
    created_item: AccountResponse
