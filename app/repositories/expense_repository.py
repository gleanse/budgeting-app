from sqlmodel import Session, select, func
from decimal import Decimal
from app.models import Expense, Category, Account


class ExpenseRepository:
    def __init__(self, session: Session):
        self.session = session

    def exists_by_category(self, category_id: int) -> bool:
        statement = select(Expense).where(Expense.category_id == category_id)
        return self.session.exec(statement).first() is not None

    def exists_by_account(self, account_id: int) -> bool:
        statement = select(Expense).where(Expense.account_id == account_id)
        return self.session.exec(statement).first() is not None

    def get_all_by_user(self, user_id: int) -> list[Expense]:
        statement = select(Expense).where(Expense.user_id == user_id)
        return self.session.exec(statement).all()

    def get_total_balance_by_account(self, account_id: int) -> Decimal:
        statement = select(func.sum(Expense.amount)).where(
            Expense.account_id == account_id
        )
        result = self.session.exec(statement).first()

        return result or Decimal("0")

    def get_all_by_user_with_category(
        self, user_id: int
    ) -> list[tuple[Expense, str | None]]:
        statement = (
            select(Expense, Category.name)
            .outerjoin(Category)
            .where(Expense.user_id == user_id)
        )

        return self.session.exec(statement).all()

    def get_all_by_user_with_category_and_account(
        self, user_id: int
    ) -> list[tuple[Expense, str | None, str | None]]:
        statement = (
            select(Expense, Category.name, Account.name)
            .outerjoin(Category, Expense.category_id == Category.id)
            .outerjoin(Account, Expense.account_id == Account.id)
            .where(Expense.user_id == user_id)
        )
        return self.session.exec(statement).all()

    def get_by_id_and_user(self, expense_id: int, user_id: int) -> Expense | None:
        statement = select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == user_id,
        )

        return self.session.exec(statement).first()

    def get_by_id_and_user_with_category_and_account(
        self, expense_id: int, user_id: int
    ) -> tuple[Expense, str | None, str | None] | None:
        statement = (
            select(Expense, Category.name, Account.name)
            .outerjoin(Category, Expense.category_id == Category.id)
            .outerjoin(Account, Expense.account_id == Account.id)
            .where(Expense.user_id == user_id, Expense.id == expense_id)
        )
        return self.session.exec(statement).first()

    def save(self, expense: Expense) -> Expense:
        """insert or update expense"""
        self.session.add(expense)
        self.session.commit()
        self.session.refresh(expense)

        return expense

    def delete(self, expense: Expense) -> None:
        self.session.delete(expense)
        self.session.commit()
