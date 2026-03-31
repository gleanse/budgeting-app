from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated
from app.database import get_session
from app.core.auth_core import get_current_user
from app.models import User, Income, Category
from app.schemas.income_schema import IncomeCreate, IncomeResponse, IncomeCreateResponse

router = APIRouter()

DatabaseSession = Annotated[Session, Depends(get_session)]
UserAuthentication = Annotated[User, Depends(get_current_user)]

@router.get("/incomes", response_model=list[IncomeResponse])
async def get_incomes(session: DatabaseSession, current_user: UserAuthentication):
    statement = select(Income, Category.name).outerjoin(Category).where(Income.user_id == current_user.id)
    results = session.exec(statement).all()

    incomes = []
    for income, category_name in results:
        incomes.append({
            "id": income.id,
            "amount": income.amount,
            "category_id": income.category_id or 0,
            "category_name": category_name or "Uncategorized (OLD DATA)",
            "description": income.description,
            "date_time": income.date_time
        })

    return incomes

@router.post("/incomes", response_model=IncomeCreateResponse)
async def create_income(session: DatabaseSession, income_data: IncomeCreate, current_user: UserAuthentication):
    if income_data.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be positive",
        )
    
    statement = select(Category).where(
        Category.id == income_data.category_id,
        Category.user_id == current_user.id
    )
    category = session.exec(statement).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    elif category.type == "expense":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category use income category",
        )

    new_income = Income(
        amount=income_data.amount,
        category_id=income_data.category_id,
        description=income_data.description,
        user_id=current_user.id,
    )

    session.add(new_income)
    session.commit()
    session.refresh(new_income)

    category = session.get(Category, new_income.category_id)

    return IncomeCreateResponse(
        income=IncomeResponse(
            id=new_income.id,
            amount=new_income.amount,
            category_id=new_income.category_id,
            category_name=category.name if category else "",
            description=new_income.description,
            date_time=new_income.date_time,
        )
    )

@router.delete("/incomes/{income_id}")
async def delete_income(session: DatabaseSession, current_user: UserAuthentication, income_id: int):
    statement = select(Income).where(
        Income.id == income_id,
        Income.user_id == current_user.id,
    )
    income = session.exec(statement).first()

    if not income:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Income record not found",
        )
    
    deleted_income = {
        "id": income.id,
        "amount": income.amount,
        "category_id": income.category_id,
    }

    session.delete(income)
    session.commit()

    return {
        "message": "Income record deleted successfully",
        "deleted_item": deleted_income,
    }