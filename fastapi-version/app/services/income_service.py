from sqlmodel import Session
from app.repositories.income_repository import IncomeRepository

class IncomeService:
    def __init__(self, session: Session):
        self.income_repo = IncomeRepository(session)

    def get_user_income(self, user_id: int) -> list[dict]:
        results = self.income_repo.get_user_income(user_id)
        
        incomes = [
            {
                "id": income.id,
                "amount": income.amount,
                "category_id": income.category_id or 0,
                "category_name": category_name or "Uncategorized",
                "description": income.description,
                "date_time": income.date_time
            }
            for income, category_name in results
        ]

        return incomes

