from sqlmodel import Session
from app.models import Account
from decimal import Decimal
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

    def get_by_id_and_user(self, account_id: int, user_id: int) -> Account:
        account = self.account_repo.get_by_id_and_user(account_id, user_id)

        if account is None:
            raise ValueError("Account not found")

        return account

    def account_balance(self, account_id: int, user_id: int) -> Decimal:
        account = self.account_repo.get_by_id_and_user(account_id, user_id)
        if account is None:
            raise ValueError("Account not found")

        total_income = self.income_repo.get_total_balance_by_account(account_id)
        total_expense = self.expense_repo.get_total_balance_by_account(account_id)

        return account.initial_balance + total_income - total_expense

    def total_balance(self, user_id: int) -> Decimal:
        # TODO: total balance of user across all accounts
        pass

    def create(self, name: str, initial_balance: Decimal, user_id: int) -> Account:
        new_account = Account(
            name=name, initial_balance=initial_balance, user_id=user_id
        )

        return self.account_repo.save(new_account)

    def update(self, account_id: int, user_id: int, name: str | None) -> Account:
        account = self.account_repo.get_by_id_and_user(account_id, user_id)

        if account is None:
            raise ValueError("Account not found")

        if name is not None:
            account.name = name

        return self.account_repo.save(account)

    def delete(self, account_id: int, user_id: int) -> None:
        account = self.account_repo.get_by_id_and_user(account_id, user_id)

        if account is None:
            raise ValueError("Account not found")

        if self.income_repo.exists_by_account(
            account_id
        ) or self.expense_repo.exists_by_account(account_id):
            raise ValueError("Cannot delete account that is in use")

        self.account_repo.delete(account)
