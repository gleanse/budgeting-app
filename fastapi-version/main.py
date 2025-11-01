from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, SQLModel, select, func
from contextlib import asynccontextmanager
from typing import Annotated
from database import engine, get_session
from auth import create_access_token, get_current_user

# NOTE: import models to register them with SQLModels metadata
# without this import, create_all() wont know which tables to create so despite its show its not being use its still important to import models
from models import User, Income, Expense
from auth_schemas import UserCreate, RegisterResponse, UserResponse
from schemas import (
    IncomeCreate,
    IncomeResponse,
    IncomeCreateResponse,
    ExpenseCreate,
    ExpenseResponse,
    ExpenseCreateResponse,
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
    statement = select(Income).where(Income.user_id == current_user.id)
    # we use all here to get all records rows not only first() row
    incomes = session.exec(statement).all()

    return incomes

@app.post("/incomes", response_model=IncomeCreateResponse)
async def create_income(session: DatabaseSession, income_data: IncomeCreate, current_user: UserAuthentication):
    if income_data.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be positive",
        )

    new_income = Income(
        amount=income_data.amount,
        category=income_data.category,
        description=income_data.description,
        user_id=current_user.id,
    )

    session.add(new_income)
    session.commit()
    session.refresh(new_income)

    return IncomeCreateResponse(
        income=IncomeResponse(
            id=new_income.id,
            amount=new_income.amount,
            category=new_income.category,
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
        "category": income.category,
    }

    session.delete(income)
    session.commit()

    return {
        "message": "Income record deleted successfully",
        "deleted_item": deleted_income,
    }

@app.get("/expenses", response_model=list[ExpenseResponse])
async def get_expenses(session: DatabaseSession, current_user: UserAuthentication):
    statement = select(Expense).where(Expense.user_id == current_user.id)

    expenses = session.exec(statement).all()

    return expenses

@app.post("/expenses", response_model=ExpenseCreateResponse)
async def create_expense(session: DatabaseSession, expense_data:ExpenseCreate, current_user:UserAuthentication):
    if expense_data.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be positive",
        )
    
    new_expense = Expense(
        amount=expense_data.amount,
        category=expense_data.category,
        description=expense_data.description,
        user_id=current_user.id,
    )

    session.add(new_expense)
    session.commit()
    session.refresh(new_expense)

    return ExpenseCreateResponse(
         expense=ExpenseResponse(
            id=new_expense.id,
            amount=new_expense.amount,
            category=new_expense.category,
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
        "category": expense.category,
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
