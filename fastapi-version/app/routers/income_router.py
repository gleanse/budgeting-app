from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated
from app.database import get_session
from app.core.auth_core import get_current_user
from app.models import User
from app.schemas.income_schema import (
    IncomeCreate,
    IncomeResponse,
    IncomeCreateResponse,
    IncomeDelete,
    IncomeDeleteResponse,
)
from app.services.income_service import IncomeService

router = APIRouter()

DatabaseSession = Annotated[Session, Depends(get_session)]
UserAuthentication = Annotated[User, Depends(get_current_user)]


@router.get("/incomes", response_model=list[IncomeResponse])
async def get_incomes(session: DatabaseSession, current_user: UserAuthentication):
    income_service = IncomeService(session)

    incomes = income_service.list_by_user(current_user.id)

    return [
        IncomeResponse(
            id=income.id,
            amount=income.amount,
            category_id=income.category_id or 0,
            category_name=income.category.name if income.category else "Uncategorized",
            description=income.description,
            date_time=income.date_time,
        )
        for income in incomes
    ]


@router.post(
    "/incomes", response_model=IncomeCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_income(
    session: DatabaseSession,
    income_data: IncomeCreate,
    current_user: UserAuthentication,
):
    income_service = IncomeService(session)

    try:
        created_income = income_service.create(
            amount=income_data.amount,
            category_id=income_data.category_id,
            description=income_data.description,
            user_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return IncomeCreateResponse(
        message="Income created successfully",
        income=IncomeResponse(
            id=created_income.id,
            amount=created_income.amount,
            category_id=created_income.category_id,
            category_name=created_income.category.name,
            description=created_income.description,
            date_time=created_income.date_time,
        ),
    )


@router.delete("/incomes/{income_id}", response_model=IncomeDeleteResponse)
async def delete_income(
    session: DatabaseSession, current_user: UserAuthentication, income_id: int
):
    income_service = IncomeService(session)

    try:
        deleted_income = income_service.delete(income_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return IncomeDeleteResponse(
        message="Income record deleted successfully",
        deleted_item=IncomeDelete(
            id=deleted_income.id,
            amount=deleted_income.amount,
            category_id=deleted_income.category_id,
        ),
    )
