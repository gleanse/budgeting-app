from sqlmodel import Session, select
from app.models import Expense, Category


class ExpenseRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_by_user_with_category(
        self, user_id: int
    ) -> list[tuple[Expense, str | None]]:
        statement = (
            select(Expense, Category.name)
            .outerjoin(Category)
            .where(Expense.user_id == user_id)
        )

        return self.session.exec(statement).all()

    def get_by_id_and_user(self, expense_id: int, user_id: int) -> Expense | None:
        statement = select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == user_id,
        )

        return self.session.exec(statement).first()

    def add(self, expense: Expense) -> Expense:
        self.session.add(expense)
        self.session.commit()
        self.session.refresh(expense)

        return expense

    def delete(self, expense: Expense):
        self.session.delete(expense)
        self.session.commit()
