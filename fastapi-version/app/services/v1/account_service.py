from sqlmodel import Session
from app.models import Account
from app.repositories.account_repository import AccountRepository
from app.repositories.income_repository import IncomeRepository
from app.repositories.expense_repository import ExpenseRepository


class AccountService:
    def __init__(self, session: Session):
        self.account_repo = AccountRepository(session)
        self.income_repo = IncomeRepository(session)
        self.expense_repo = ExpenseRepository(session)

    def list_by_user(self, user_id: int) -> list[Account]:
        return self.account_repo.get_all_by_user(user_id)

    def account_balance(self, user_id: int) -> float:
        incomes = self.income_repo.get_all_by_user(user_id)
        total_income = sum(income.amount for income in incomes)

        expenses = self.expense_repo.get_all_by_user(user_id)
        total_expense = sum(expense.amount for expense in expenses)

        return total_income - total_expense
