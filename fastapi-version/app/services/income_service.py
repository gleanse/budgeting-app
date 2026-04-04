from sqlmodel import Session
from app.models import Income
from app.repositories.income_repository import IncomeRepository
from app.repositories.category_repository import CategoryRepository

class IncomeService:
    def __init__(self, session: Session):
        self.income_repo = IncomeRepository(session)
        self.category_repo = CategoryRepository(session)

    def list_by_user(self, user_id: int) -> list[Income]:
        incomes = self.income_repo.get_all_by_user(user_id)
        return incomes
    
    def create(self, amount: float, category_id: int, description: str, user_id: int) -> Income:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        category = self.category_repo.get_by_id_and_user(category_id, user_id)

        if not category:
            raise ValueError("Category not found")
        elif category.type == "expense":
            raise ValueError("Invalid category use income category")
        
        new_income = Income(
            amount=amount,
            category_id=category_id,
            description=description,
            user_id=user_id,
        )
        self.income_repo.add(new_income)

        return new_income

    def delete(self, income_id: int, user_id: int) -> Income:
        income = self.income_repo.get_by_id_and_user(income_id, user_id)

        if not income:
            raise ValueError("Income record not found")
        self.income_repo.delete(income)

        return income
