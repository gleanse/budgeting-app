from fastapi import APIRouter, HTTPException, status
from app.core.dependencies import UserAuthenticationDep, TransactionServiceDep
from app.schemas.v1.expense_schema import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseCreateResponse,
    ExpenseDelete,
    ExpenseDeleteResponse,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=list[ExpenseResponse])
async def get_expenses(
    current_user: UserAuthenticationDep, transaction_service: TransactionServiceDep
):

    try:
        expenses = transaction_service.list_by_user("expense", current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return [
        ExpenseResponse(
            id=expense.id,
            amount=expense.amount,
            category_id=expense.category_id or 0,
            category_name=category_name if category_name else "Uncategorized",
            description=expense.description,
            date_time=expense.date_time,
        )
        for expense, category_name in expenses
    ]


@router.post("/", response_model=ExpenseCreateResponse)
async def create_expense(
    current_user: UserAuthenticationDep,
    transaction_service: TransactionServiceDep,
    expense_data: ExpenseCreate,
):

    try:
        created_expense, category_name = transaction_service.create(
            transaction_type="expense",
            amount=expense_data.amount,
            category_id=expense_data.category_id,
            description=expense_data.description,
            user_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return ExpenseCreateResponse(
        message="Expense created successfully",
        expense=ExpenseResponse(
            id=created_expense.id,
            amount=created_expense.amount,
            category_id=created_expense.category_id,
            category_name=category_name if category_name else "Uncategorized",
            description=created_expense.description,
            date_time=created_expense.date_time,
        ),
    )


@router.delete("/{expense_id}")
async def delete_expense(
    current_user: UserAuthenticationDep,
    transaction_service: TransactionServiceDep,
    expense_id: int,
):
    try:
        deleted_expense = transaction_service.delete(
            transaction_type="expense",
            transaction_id=expense_id,
            user_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return ExpenseDeleteResponse(
        message="Expense record deleted successfully",
        deleted_item=ExpenseDelete(
            id=deleted_expense.id,
            amount=deleted_expense.amount,
            category_id=deleted_expense.category_id,
        ),
    )
