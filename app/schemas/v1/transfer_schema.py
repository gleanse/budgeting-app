from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class TransferCreateRequest(BaseModel):
    amount: Decimal
    from_account_id: int
    to_account_id: int
    description: str | None = None
    date_time: datetime | None = None


class TransferPatchRequest(BaseModel):
    amount: Decimal | None = None
    from_account_id: int | None = None
    to_account_id: int | None = None
    description: str | None = None
    date_time: datetime | None = None


class TransferListResponse(BaseModel):
    id: int
    amount: Decimal
    from_account_name: str
    to_account_name: str
    date_time: datetime


class TransferDetailResponse(BaseModel):
    id: int
    amount: Decimal
    from_account_id: int
    from_account_name: str
    to_account_id: int
    to_account_name: str
    description: str | None
    date_time: datetime


class TransferCreateResponse(BaseModel):
    message: str = "Transfer created successfully"
    created_item: TransferDetailResponse
