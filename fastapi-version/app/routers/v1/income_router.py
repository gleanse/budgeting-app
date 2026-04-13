from fastapi import APIRouter, HTTPException, status
from app.core.dependencies import UserAuthenticationDep, TransactionServiceDep
from app.schemas.v1.income_schema import (
    IncomeCreate,
    IncomeResponse,
    IncomeCreateResponse,
    IncomeDelete,
    IncomeDeleteResponse,
)

router = APIRouter(prefix="/incomes", tags=["incomes"])


@router.get("/", response_model=list[IncomeResponse])
async def get_incomes(
    current_user: UserAuthenticationDep, transaction_service: TransactionServiceDep
) -> list[IncomeResponse]:

    try:
        incomes = transaction_service.list_by_user("income", current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return [
        IncomeResponse(
            id=income.id,
            amount=income.amount,
            category_id=income.category_id or 0,
            category_name=category_name if category_name else "Uncategorized",
            account_id=income.account_id,
            account_name=account_name if account_name else "Cash",
            description=income.description,
            date_time=income.date_time,
        )
        for income, category_name, account_name in incomes
    ]


@router.post(
    "/", response_model=IncomeCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_income(
    current_user: UserAuthenticationDep,
    transaction_service: TransactionServiceDep,
    income_data: IncomeCreate,
) -> IncomeCreateResponse:

    try:
        created_income, category_name, account_name = transaction_service.create(
            transaction_type="income",
            amount=income_data.amount,
            category_id=income_data.category_id,
            account_id=income_data.account_id,
            description=income_data.description,
            user_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return IncomeCreateResponse(
        income=IncomeResponse(
            id=created_income.id,
            amount=created_income.amount,
            category_id=created_income.category_id,
            category_name=category_name if category_name else "Uncategorized",
            account_id=created_income.account_id,
            account_name=account_name if account_name else "Cash",
            description=created_income.description,
            date_time=created_income.date_time,
        ),
    )


@router.delete("/{income_id}", response_model=IncomeDeleteResponse)
async def delete_income(
    current_user: UserAuthenticationDep,
    transaction_service: TransactionServiceDep,
    income_id: int,
) -> IncomeDeleteResponse:

    try:
        deleted_income = transaction_service.delete(
            transaction_type="income",
            transaction_id=income_id,
            user_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return IncomeDeleteResponse(
        deleted_item=IncomeDelete(
            id=deleted_income.id,
            amount=deleted_income.amount,
            category_id=deleted_income.category_id,
        ),
    )
