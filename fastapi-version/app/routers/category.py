from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated
from app.database import get_session
from app.core.auth import get_current_user
from app.models import User, Category, Income, Expense
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryCreateResponse

router = APIRouter()

DatabaseSession = Annotated[Session, Depends(get_session)]
UserAuthentication = Annotated[User, Depends(get_current_user)]

@router.get("/categories", response_model=list[CategoryResponse])
async def get_categories(session: DatabaseSession, current_user: UserAuthentication):
    statement = select(Category).where(Category.user_id == current_user.id)
    categories = session.exec(statement).all()
    return categories

@router.post("/categories", response_model=CategoryCreateResponse)
async def create_category(session: DatabaseSession, category_data: CategoryCreate, current_user: UserAuthentication):
    new_category = Category(
        name=category_data.name,
        type=category_data.type,
        user_id=current_user.id,
    )

    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    return CategoryCreateResponse(
        category=CategoryResponse(
            id=new_category.id,
            name=new_category.name,
            type=new_category.type,
            user_id=new_category.user_id,
        )
    )

@router.delete("/categories/{category_id}")
async def delete_category(session: DatabaseSession, current_user: UserAuthentication, category_id: int):
    statement = select(Category).where(
        Category.id == category_id,
        Category.user_id == current_user.id,
    )
    category = session.exec(statement).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    income_count = session.exec(
        select(Income).where(Income.category_id == category_id)
    ).first()

    expense_count = session.exec(
        select(Expense).where(Expense.category_id == category_id)
    ).first()

    if income_count or expense_count:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category that is being used by income or expense records"
        )
    
    deleted_category = {
        "id": category.id,
        "name": category.name,
        "type": category.type,
    }

    session.delete(category)
    session.commit()

    return {
        "message": "Category deleted successfully",
        "deleted_item": deleted_category,
    }