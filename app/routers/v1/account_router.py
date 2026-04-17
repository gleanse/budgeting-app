from fastapi import APIRouter
from app.core.dependencies import UserAuthenticationDep, AccountServiceDep
from app.schemas.v1.account_schema import AccountResponse, AccountBalanceResponse

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=list[AccountResponse])
async def get_my_accounts(
    current_user: UserAuthenticationDep, account_service: AccountServiceDep
):
    return account_service.list_by_user(current_user.id)


@router.get("/balance", response_model=AccountBalanceResponse)
async def get_total_balance(
    current_user: UserAuthenticationDep, account_service: AccountServiceDep
):
    balance = account_service.account_balance(current_user.id)
    return AccountBalanceResponse(total_balance=balance)
