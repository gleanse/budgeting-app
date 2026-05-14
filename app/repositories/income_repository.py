from sqlmodel import Session, select, func
from decimal import Decimal
from app.models import Income, Category, Account


class IncomeRepository:
    def __init__(self, session: Session):
        self.session = session

    def exists_by_category(self, category_id: int) -> bool:
        statement = select(Income).where(Income.category_id == category_id)
        return self.session.exec(statement).first() is not None

    def exists_by_account(self, account_id: int) -> bool:
        statement = select(Income).where(Income.account_id == account_id)
        return self.session.exec(statement).first() is not None

    def get_all_by_user(self, user_id: int) -> list[Income]:
        statement = select(Income).where(Income.user_id == user_id)
        return self.session.exec(statement).all()

    def get_total_balance_across_accounts_by_user(self, user_id: int) -> Decimal:
        statement = select(func.sum(Income.amount)).where(Income.user_id == user_id)
        result = self.session.exec(statement).first()

        return result or Decimal("0")

    def get_total_balance_by_account(self, account_id: int) -> Decimal:
        statement = select(func.sum(Income.amount)).where(
            Income.account_id == account_id
        )
        result = self.session.exec(statement).first()

        return result or Decimal("0")

    def get_all_by_user_with_category(
        self, user_id: int
    ) -> list[tuple[Income, str | None]]:
        statement = (
            select(Income, Category.name)
            .outerjoin(Category)
            .where(Income.user_id == user_id)
        )

        return self.session.exec(statement).all()

    def get_all_by_user_with_category_and_account(
        self, user_id: int
    ) -> list[tuple[Income, str | None, str | None]]:
        statement = (
            select(Income, Category.name, Account.name)
            .outerjoin(Category, Income.category_id == Category.id)
            .outerjoin(Account, Income.account_id == Account.id)
            .where(Income.user_id == user_id)
        )
        return self.session.exec(statement).all()

    def get_by_id_and_user(self, income_id: int, user_id: int) -> Income | None:
        statement = select(Income).where(
            Income.id == income_id,
            Income.user_id == user_id,
        )

        return self.session.exec(statement).first()

    def get_by_id_and_user_with_category_and_account(
        self, income_id: int, user_id: int
    ) -> tuple[Income, str | None, str | None] | None:
        statement = (
            select(Income, Category.name, Account.name)
            .outerjoin(Category, Income.category_id == Category.id)
            .outerjoin(Account, Income.account_id == Account.id)
            .where(Income.user_id == user_id, Income.id == income_id)
        )
        return self.session.exec(statement).first()

    def save(self, income: Income) -> Income:
        """insert or update income"""
        self.session.add(income)
        self.session.commit()
        self.session.refresh(income)

        return income

    def delete(self, income: Income) -> None:
        self.session.delete(income)
        self.session.commit()
