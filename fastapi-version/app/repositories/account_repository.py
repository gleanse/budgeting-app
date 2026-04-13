from sqlmodel import Session, select
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

    def add(self, account: Account) -> Account:
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)

        return account
