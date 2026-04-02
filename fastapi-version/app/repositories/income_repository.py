from sqlmodel import Session, select
from app.models import Income, Category, User

class IncomeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_income(self, user_id: int) -> list[tuple[Income, str | None]]:
        statement = select(Income, Category.name).outerjoin(Category).where(Income.user_id == user_id)
        return self.session.exec(statement).all()