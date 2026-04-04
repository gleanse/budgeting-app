from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated
from app.database import get_session
from app.core.auth_core import get_current_user
from app.models import User, Expense, Category
from app.schemas.expense_schema import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseCreateResponse,
)

router = APIRouter()

DatabaseSession = Annotated[Session, Depends(get_session)]
UserAuthentication = Annotated[User, Depends(get_current_user)]


@router.get("/expenses", response_model=list[ExpenseResponse])
async def get_expenses(session: DatabaseSession, current_user: UserAuthentication):
    statement = (
        select(Expense, Category.name)
        .outerjoin(Category)
        .where(Expense.user_id == current_user.id)
    )
    results = session.exec(statement).all()

    expenses = []
    for expense, category_name in results:
        expenses.append(
            {
                "id": expense.id,
                "amount": expense.amount,
                "category_id": expense.category_id or 0,
                "category_name": category_name or "Uncategorized (OLD DATA)",
                "description": expense.description,
                "date_time": expense.date_time,
            }
        )

    return expenses


@router.post("/expenses", response_model=ExpenseCreateResponse)
async def create_expense(
    session: DatabaseSession,
    expense_data: ExpenseCreate,
    current_user: UserAuthentication,
):
    if expense_data.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be positive",
        )

    statement = select(Category).where(
        Category.id == expense_data.category_id,
        Category.user_id == current_user.id,
    )
    category = session.exec(statement).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    elif category.type == "income":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category use expense category",
        )

    new_expense = Expense(
        amount=expense_data.amount,
        category_id=expense_data.category_id,
        description=expense_data.description,
        user_id=current_user.id,
    )

    session.add(new_expense)
    session.commit()
    session.refresh(new_expense)

    category = session.get(Category, new_expense.category_id)

    return ExpenseCreateResponse(
        expense=ExpenseResponse(
            id=new_expense.id,
            amount=new_expense.amount,
            category_id=new_expense.category_id,
            category_name=category.name if category else "",
            description=new_expense.description,
            date_time=new_expense.date_time,
        )
    )


@router.delete("/expenses/{expense_id}")
async def delete_expense(
    session: DatabaseSession, current_user: UserAuthentication, expense_id: int
):
    statement = select(Expense).where(
        Expense.id == expense_id,
        Expense.user_id == current_user.id,
    )
    expense = session.exec(statement).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense record not found",
        )

    deleted_expense = {
        "id": expense.id,
        "amount": expense.amount,
        "category_id": expense.category_id,
    }

    session.delete(expense)
    session.commit()

    return {
        "message": "Expense record deleted successfully",
        "deleted_item": deleted_expense,
    }
