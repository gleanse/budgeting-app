from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, SQLModel, select, func
from contextlib import asynccontextmanager
from typing import Annotated
from database import engine, get_session
from auth import create_access_token, get_current_user

# NOTE: import models to register them with SQLModels metadata
# without this import, create_all() wont know which tables to create so despite its show its not being use its still important to import models
from models import (
    User,
    Income,
    Expense,
    Category,
)
from auth_schemas import UserCreate, RegisterResponse, UserResponse
from schemas import (
    IncomeCreate,
    IncomeResponse,
    IncomeCreateResponse,
    ExpenseCreate,
    ExpenseResponse,
    ExpenseCreateResponse,
    CategoryCreate,
    CategoryResponse,
    CategoryCreateResponse,
)


# STARTUP code that will first to run when server starts
# create all the database tables during start of the server, if the table already exist it will just ignore it
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("SERVER - Server running...")
    print(f"Models registered: {SQLModel.metadata.tables.keys()}")
    SQLModel.metadata.create_all(engine)
    print("DATABASE - All database tables created")
    yield
    print("SERVER - Shutting down...")

app = FastAPI(lifespan=lifespan)

DatabaseSession = Annotated[Session, Depends(get_session)]
UserAuthentication =  Annotated[User, Depends(get_current_user)]


@app.get("/")
async def root():
    print("Server Running")

    return {"message": "Budgeting App v0.1"}

@app.post("/register", response_model=RegisterResponse)
async def register_user(session: DatabaseSession, user_data: UserCreate):
    statement = select(User).where(User.username == user_data.username)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    
    new_user = User(username=user_data.username)
    new_user.set_password(user_data.password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return RegisterResponse(
        user=UserResponse(id=new_user.id, username=new_user.username),
        message="User created successfully",
    )

@app.post("/login")
async def login(session: DatabaseSession, form_data: OAuth2PasswordRequestForm = Depends()):
    # find user by username in database using orm sqlalchemy
    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()

    # validate user exists and password is correct
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # generate token for the user
    access_token = create_access_token(username=user.username)

    return {"access_token": access_token, "token_type": "bearer"}

# TODO: simple logout endpoints for now since literally logout happeneds on frontend but for future enhancements/refactors add a blacklisted token for those who logged out but the token still valid and not expired
@app.post("/logout")
async def logout(session: DatabaseSession, current_user: UserAuthentication):
    return {"message": "Successfully logged out"}

@app.get("/incomes", response_model=list[IncomeResponse])
async def get_incomes(session: DatabaseSession, current_user: UserAuthentication):
    # joining the category name for frontend use i use outerjoin for now since i do have old data that are null
    # TODO: use normal join later
    statement = select(Income, Category.name).outerjoin(Category).where(Income.user_id == current_user.id)
    # we use all here to get all records rows not only first() row
    results = session.exec(statement).all()

    incomes = []

    # reformatting each db rows into dict
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

@app.post("/incomes", response_model=IncomeCreateResponse)
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

    # validation checking if the category id input is existing and belong to income category
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

@app.delete("/incomes/{income_id}")
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

@app.get("/expenses", response_model=list[ExpenseResponse])
async def get_expenses(session: DatabaseSession, current_user: UserAuthentication):
    statement = select(Expense, Category.name).outerjoin(Category).where(Expense.user_id == current_user.id)
    results = session.exec(statement).all()

    expenses = []

    for expense, category_name in results:
        expenses.append({
            "id": expense.id,
            "amount": expense.amount,
            "category_id": expense.category_id or 0,
            "category_name": category_name or "Uncategorized (OLD DATA)",
            "description": expense.description,
            "date_time": expense.date_time
        })

    return expenses

@app.post("/expenses", response_model=ExpenseCreateResponse)
async def create_expense(session: DatabaseSession, expense_data:ExpenseCreate, current_user:UserAuthentication):
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

    # validation checking if the category id input is existing and belong to expense category
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

@app.delete("/expenses/{expense_id}")
async def delete_expense(session: DatabaseSession, current_user: UserAuthentication, expense_id: int):
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

@app.get("/balance")
async def get_balance(session: DatabaseSession, current_user: UserAuthentication):
    # calculating sum of all income
    income_statement = select(func.sum(Income.amount)).where(Income.user_id == current_user.id)
    total_income = session.exec(income_statement).first() or 0

    # calculating sum of all expenses
    expense_statement = select(func.sum(Expense.amount)).where(Expense.user_id == current_user.id)
    total_expenses = session.exec(expense_statement).first() or 0

    balance = total_income - total_expenses

    return {
        "balance": balance,
        "total_income": total_income,
        "total_expenses": total_expenses,
    }

@app.get("/categories", response_model=list[CategoryResponse])
async def get_categories(session: DatabaseSession, current_user: UserAuthentication):
    statement = select(Category).where(Category.user_id == current_user.id)
    categories = session.exec(statement).all()

    return categories

@app.post("/categories", response_model=CategoryCreateResponse)
async def create_category(session: DatabaseSession, category_data: CategoryCreate, current_user: UserAuthentication):
    if category_data.type not in ["income", "expense"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type must be 'income' or 'expense'"
        )
    
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

@app.delete("/categories/{category_id}")
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
    
    # check if the category is being used
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
