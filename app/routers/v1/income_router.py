from fastapi import APIRouter, HTTPException, status
from app.core.dependencies import UserAuthenticationDep, TransactionServiceDep
from app.schemas.v1.income_schema import (
    IncomeCreateRequest,
    IncomeUpdateRequest,
    IncomeListResponse,
    IncomeDetailResponse,
    IncomeCreateResponse,
)

router = APIRouter(prefix="/incomes", tags=["incomes"])


@router.get("/", response_model=list[IncomeListResponse])
async def get_incomes(
    current_user: UserAuthenticationDep, transaction_service: TransactionServiceDep
) -> list[IncomeListResponse]:

    try:
        incomes = transaction_service.list_by_user("income", current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return [
        IncomeListResponse(
            id=income.id,
            amount=income.amount,
            category_name=category_name if category_name else "Uncategorized",
            account_name=account_name if account_name else "Cash",
            date_time=income.date_time,
        )
        for income, category_name, account_name in incomes
    ]


@router.get("/{income_id}", response_model=IncomeDetailResponse)
async def get_income(
    current_user: UserAuthenticationDep,
    transaction_service: TransactionServiceDep,
    income_id: int,
) -> IncomeDetailResponse:
    try:
        income, category_name, account_name = (
            transaction_service.get_detail_by_id_and_user(
                transaction_type="income",
                transaction_id=income_id,
                user_id=current_user.id,
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return IncomeDetailResponse(
        id=income.id,
        amount=income.amount,
        category_id=income.category_id or 0,
        category_name=category_name if category_name else "Uncategorized",
        account_id=income.account_id,
        account_name=account_name if account_name else "Cash",
        description=income.description,
        date_time=income.date_time,
    )


@router.post(
    "/", response_model=IncomeCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_income(
    current_user: UserAuthenticationDep,
    transaction_service: TransactionServiceDep,
    income_data: IncomeCreateRequest,
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
        income=IncomeDetailResponse(
            id=created_income.id,
            amount=created_income.amount,
            category_id=created_income.category_id or 0,
            category_name=category_name if category_name else "Uncategorized",
            account_id=created_income.account_id,
            account_name=account_name if account_name else "Cash",
            description=created_income.description,
            date_time=created_income.date_time,
        ),
    )


@router.patch("/{income_id}", response_model=IncomeDetailResponse)
async def update_income(
    current_user: UserAuthenticationDep,
    transaction_service: TransactionServiceDep,
    income_id: int,
    income_data: IncomeUpdateRequest,
) -> IncomeDetailResponse:
    try:
        update_data = income_data.model_dump(exclude_none=True)

        updated_transaction, category_name, account_name = transaction_service.update(
            transaction_id=income_id,
            user_id=current_user.id,
            **update_data,
        )
    except ValueError as e:
        if "Transaction not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return IncomeDetailResponse(
        id=updated_transaction.id,
        amount=updated_transaction.amount,
        category_id=updated_transaction.category_id,
        category_name=category_name if category_name else "Uncategorized",
        account_id=updated_transaction.account_id,
        account_name=account_name if account_name else "Cash",
        description=updated_transaction.description,
        date_time=updated_transaction.date_time,
    )


@router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_income(
    current_user: UserAuthenticationDep,
    transaction_service: TransactionServiceDep,
    income_id: int,
) -> None:
    try:
        transaction_service.delete(
            transaction_type="income",
            transaction_id=income_id,
            user_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return None
