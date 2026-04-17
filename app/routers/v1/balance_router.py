from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from typing import Annotated
from app.database import get_session
from app.core.auth_core import get_current_user
from app.models import User, Income, Expense

router = APIRouter(prefix="/balance", tags=["balance"])

DatabaseSession = Annotated[Session, Depends(get_session)]
UserAuthentication = Annotated[User, Depends(get_current_user)]


@router.get("/")
async def get_balance(session: DatabaseSession, current_user: UserAuthentication):
    income_statement = select(func.sum(Income.amount)).where(
        Income.user_id == current_user.id
    )
    total_income = session.exec(income_statement).first() or 0

    expense_statement = select(func.sum(Expense.amount)).where(
        Expense.user_id == current_user.id
    )
    total_expenses = session.exec(expense_statement).first() or 0

    balance = total_income - total_expenses

    return {
        "balance": balance,
        "total_income": total_income,
        "total_expenses": total_expenses,
    }
