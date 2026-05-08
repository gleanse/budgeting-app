from fastapi import APIRouter, HTTPException, status
from app.core.dependencies import UserAuthenticationDep, TransactionServiceDep
from app.schemas.v1.expense_schema import (
    ExpenseCreateRequest,
    ExpenseUpdateRequest,
    ExpenseListResponse,
    ExpenseDetailResponse,
    ExpenseCreateResponse,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=list[ExpenseListResponse])
async def get_expenses(
    current_user: UserAuthenticationDep, transaction_service: TransactionServiceDep
) -> list[ExpenseListResponse]:
    expenses = transaction_service.list_by_user("expense", current_user.id)

    return [
        ExpenseListResponse(
            id=expense.id,
            amount=expense.amount,
            category_name=category_name if category_name else "Uncategorized",
            account_name=account_name if account_name else "Cash",
            date_time=expense.date_time,
        )
        for expense, category_name, account_name in expenses
    ]


@router.get("/{expense_id}", response_model=ExpenseDetailResponse)
async def get_expense(
    current_user: UserAuthenticationDep,
    transaction_service: TransactionServiceDep,
    expense_id: int,
) -> ExpenseDetailResponse:
    try:
        expense, category_name, account_name = (
            transaction_service.get_detail_by_id_and_user(
                transaction_type="expense",
                transaction_id=expense_id,
                user_id=current_user.id,
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return ExpenseDetailResponse(
        id=expense.id,
        amount=expense.amount,
        category_id=expense.category_id or 0,
        category_name=category_name if category_name else "Uncategorized",
        account_id=expense.account_id,
        account_name=account_name if account_name else "Cash",
        description=expense.description,
        date_time=expense.date_time,
    )


@router.post(
    "/", response_model=ExpenseCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_expense(
    current_user: UserAuthenticationDep,
    transaction_service: TransactionServiceDep,
    expense_data: ExpenseCreateRequest,
) -> ExpenseCreateResponse:
    try:
        created_expense, category_name, account_name = transaction_service.create(
            transaction_type="expense",
            amount=expense_data.amount,
            category_id=expense_data.category_id,
            account_id=expense_data.account_id,
            description=expense_data.description,
            user_id=current_user.id,
        )
    except ValueError as e:
        error = str(e)
        if "not found" in error.lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
        elif "invalid category" in error.lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return ExpenseCreateResponse(
        expense=ExpenseDetailResponse(
            id=created_expense.id,
            amount=created_expense.amount,
            category_id=created_expense.category_id,
            category_name=category_name if category_name else "Uncategorized",
            account_id=created_expense.account_id,
            account_name=account_name if account_name else "Cash",
            description=created_expense.description,
            date_time=created_expense.date_time,
        ),
    )


@router.patch("/{expense_id}", response_model=ExpenseDetailResponse)
async def update_expense(
    current_user: UserAuthenticationDep,
    transaction_service: TransactionServiceDep,
    expense_id: int,
    expense_data: ExpenseUpdateRequest,
) -> ExpenseDetailResponse:
    try:
        update_data = expense_data.model_dump(exclude_none=True)

        updated_transaction, category_name, account_name = transaction_service.update(
            transaction_id=expense_id,
            user_id=current_user.id,
            **update_data,
        )
    except ValueError as e:
        error = str(e)
        if "not found" in error.lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return ExpenseDetailResponse(
        id=updated_transaction.id,
        amount=updated_transaction.amount,
        category_id=updated_transaction.category_id,
        category_name=category_name if category_name else "Uncategorized",
        account_id=updated_transaction.account_id,
        account_name=account_name if account_name else "Cash",
        description=updated_transaction.description,
        date_time=updated_transaction.date_time,
    )


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    current_user: UserAuthenticationDep,
    transaction_service: TransactionServiceDep,
    expense_id: int,
) -> None:
    try:
        transaction_service.delete(
            transaction_type="expense",
            transaction_id=expense_id,
            user_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
