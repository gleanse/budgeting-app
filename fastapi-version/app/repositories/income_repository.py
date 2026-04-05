from sqlmodel import Session, select
from app.models import Income, Category


class IncomeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_by_user_with_category(
        self, user_id: int
    ) -> list[tuple[Income, str | None]]:
        statement = (
            select(Income, Category.name)
            .outerjoin(Category)
            .where(Income.user_id == user_id)
        )
        return self.session.exec(statement).all()

    def get_by_id_and_user(self, income_id: int, user_id: int) -> Income | None:
        statement = select(Income).where(
            Income.id == income_id,
            Income.user_id == user_id,
        )

        return self.session.exec(statement).first()

    def add(self, income: Income) -> Income:
        self.session.add(income)
        self.session.commit()
        self.session.refresh(income)

        return income

    def delete(self, income: Income):
        self.session.delete(income)
        self.session.commit()
