from sqlmodel import Session, select
from app.models import Category


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id_and_user(self, category_id: int, user_id: int) -> Category | None:
        statement = select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id,
        )

        return self.session.exec(statement).first()
