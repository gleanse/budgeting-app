from pydantic import BaseModel


class AccountCreate(BaseModel):
    name: str


class AccountResponse(BaseModel):
    id: int
    name: str


class AccountBalanceResponse(BaseModel):
    total_balance: float


class AccountCreateResponse(BaseModel):
    message: str = "Account created successfully"
    account: AccountResponse


class AccountDelete(BaseModel):
    id: int
    name: str


class AccountDeleteResponse(BaseModel):
    message: str = "Account deleted successfully"
    deleted_item: AccountDelete
