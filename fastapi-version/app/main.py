from fastapi import FastAPI
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from app.database import engine
from app.models import User, Income, Expense, Category
from app.routers import (
    auth_router,
    balance_router,
    category_router,
    expense_router,
    income_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("SERVER - Server running...")
    print(f"Models registered: {SQLModel.metadata.tables.keys()}")
    SQLModel.metadata.create_all(engine)
    print("DATABASE - All database tables created")
    yield
    print("SERVER - Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router.router)
app.include_router(income_router.router)
app.include_router(expense_router.router)
app.include_router(category_router.router)
app.include_router(balance_router.router)


@app.get("/")
async def root():
    return {"message": "Budgeting App v0.1"}
