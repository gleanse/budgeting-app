from sqlmodel import Session
from app.models import Income, Expense
from app.repositories.income_repository import IncomeRepository
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.category_repository import CategoryRepository


class TransactionService:
    def __init__(self, session: Session):
        self.income_repo = IncomeRepository(session)
        self.expense_repo = ExpenseRepository(session)
        self.category_repo = CategoryRepository(session)

    def list_by_user(
        self, transaction_type: str, user_id: int
    ) -> list[tuple[Income | Expense, str | None]]:
        if transaction_type == "income":
            return self.income_repo.get_all_by_user_with_category(user_id)
        elif transaction_type == "expense":
            return self.expense_repo.get_all_by_user_with_category(user_id)
        else:
            raise ValueError(f"Invalid transaction type: {transaction_type}")

    def create(
        self,
        transaction_type: str,
        amount: float,
        category_id: int,
        description: str,
        user_id: int,
    ) -> tuple[Income | Expense, str]:

        if transaction_type not in ("income", "expense"):
            raise ValueError(f"Invalid transaction type: {transaction_type}")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        category = self.category_repo.get_by_id_and_user(category_id, user_id)

        if not category:
            raise ValueError("Category not found")

        if category.type != transaction_type:
            raise ValueError(f"Invalid category, use a {transaction_type} category")

        if transaction_type == "income":
            new_transaction = Income(
                amount=amount,
                category_id=category_id,
                description=description,
                user_id=user_id,
            )
            self.income_repo.add(new_transaction)
        else:
            new_transaction = Expense(
                amount=amount,
                category_id=category_id,
                description=description,
                user_id=user_id,
            )
            self.expense_repo.add(new_transaction)

        return new_transaction, category.name

    def delete(
        self, transaction_type: str, transaction_id: int, user_id: int
    ) -> Income | Expense:

        if transaction_type == "income":
            transaction = self.income_repo.get_by_id_and_user(transaction_id, user_id)

            if not transaction:
                raise ValueError("Income record not found")

            self.income_repo.delete(transaction)
        elif transaction_type == "expense":
            transaction = self.expense_repo.get_by_id_and_user(transaction_id, user_id)

            if not transaction:
                raise ValueError("Expense record not found")

            self.expense_repo.delete(transaction)
        else:
            raise ValueError(f"Invalid transaction type: {transaction_type}")

        return transaction
