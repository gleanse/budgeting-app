from sqlmodel import Session
from app.models import Category
from app.repositories.category_repository import CategoryRepository
from app.repositories.income_repository import IncomeRepository
from app.repositories.expense_repository import ExpenseRepository


class CategoryService:
    def __init__(self, session: Session):
        self.category_repo = CategoryRepository(session)
        self.income_repo = IncomeRepository(session)
        self.expense_repo = ExpenseRepository(session)

    def list_by_user(self, user_id: int) -> list[Category]:
        return self.category_repo.get_all_by_user(user_id)

    def create(self, name: str, type: str, user_id: int) -> Category:
        if type not in ("income", "expense"):
            raise ValueError(f"Invalid transaction type: {type}")

        new_category = Category(
            name=name,
            type=type,
            user_id=user_id,
        )

        return self.category_repo.add(new_category)

    def delete(self, id: int, user_id: int) -> Category:
        category = self.category_repo.get_by_id_and_user(id, user_id)

        if not category:
            raise ValueError("Category not found")

        if self.income_repo.exists_by_category(
            id
        ) or self.expense_repo.exists_by_category(id):
            raise ValueError("Cannot delete category that is in use")

        self.category_repo.delete(category)

        return category
