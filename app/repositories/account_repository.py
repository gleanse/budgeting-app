from sqlmodel import Session, select, func
from decimal import Decimal
from app.models import Account


class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_by_user(self, user_id: int) -> list[Account]:
        statement = select(Account).where(Account.user_id == user_id)
        return self.session.exec(statement).all()

    def get_by_id_and_user(self, account_id: int, user_id: int) -> Account | None:
        statement = select(Account).where(
            Account.id == account_id, Account.user_id == user_id
        )
        return self.session.exec(statement).first()

    def get_total_initial_balance_by_user(self, user_id: int) -> Decimal:
        statement = select(func.sum(Account.initial_balance)).where(
            Account.user_id == user_id
        )
        result = self.session.exec(statement).first()

        return result or Decimal("0")

    def save(self, account: Account) -> Account:
        """insert or update account"""
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)

        return account

    def delete(self, account: Account) -> None:
        self.session.delete(account)
        self.session.commit()
