from sqlmodel import Session
from datetime import datetime
from app.models import Income, Expense
from app.repositories.income_repository import IncomeRepository
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.account_repository import AccountRepository


class TransactionService:
    def __init__(self, session: Session):
        self.income_repo = IncomeRepository(session)
        self.expense_repo = ExpenseRepository(session)
        self.category_repo = CategoryRepository(session)
        self.account_repo = AccountRepository(session)

    def list_by_user(
        self, transaction_type: str, user_id: int
    ) -> list[tuple[Income | Expense, str | None, str | None]]:
        if transaction_type == "income":
            return self.income_repo.get_all_by_user_with_category_and_account(user_id)
        elif transaction_type == "expense":
            return self.expense_repo.get_all_by_user_with_category_and_account(user_id)
        else:
            raise ValueError(f"Invalid transaction type: {transaction_type}")

    def create(
        self,
        transaction_type: str,
        amount: float,
        category_id: int,
        account_id: int,
        description: str,
        user_id: int,
        date_time: datetime | None = None,
    ) -> tuple[Income | Expense, str, str]:

        if transaction_type not in ("income", "expense"):
            raise ValueError(f"Invalid transaction type: {transaction_type}")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        category = self.category_repo.get_by_id_and_user(category_id, user_id)
        if not category:
            raise ValueError("Category not found")

        account = self.account_repo.get_by_id_and_user(account_id, user_id)
        if not account:
            raise ValueError("Account not found")

        if category.type != transaction_type:
            raise ValueError(f"Invalid category, use a {transaction_type} category")

        if transaction_type == "income":
            new_transaction = Income(
                amount=amount,
                category_id=category_id,
                account_id=account_id,
                description=description,
                user_id=user_id,
                date_time=date_time,
            )
            self.income_repo.add(new_transaction)
        else:
            new_transaction = Expense(
                amount=amount,
                category_id=category_id,
                account_id=account_id,
                description=description,
                user_id=user_id,
                date_time=date_time,
            )
            self.expense_repo.add(new_transaction)

        return new_transaction, category.name, account.name

    def update(self, transaction_id: int, user_id: int, **kwargs) -> Income | Expense:
        transaction = self.income_repo.get_by_id_and_user(transaction_id, user_id)
        is_income = True

        if not transaction:
            transaction = self.expense_repo.get_by_id_and_user(transaction_id, user_id)
            is_income = False

        if not transaction:
            raise ValueError("Transaction not found")

        # check if category type is changing
        new_category_id = kwargs.get("category_id")
        if new_category_id is not None:
            new_category = self.category_repo.get_by_id_and_user(
                new_category_id, user_id
            )
            if not new_category:
                raise ValueError("Category not found")

            expected_type = "income" if is_income else "expense"

            if new_category.type != expected_type:
                # if transaction type detected change by its new update category, delete old create new on opposite transaction type
                return self._convert_transaction(
                    transaction, new_category, user_id, **kwargs
                )

        # for normal update (if category that will update is just same type)
        for key, value in kwargs.items():
            if value is not None:
                setattr(transaction, key, value)

        if is_income:
            return self.income_repo.save(transaction)
        else:
            return self.expense_repo.save(transaction)

    def delete(self, transaction_id: int, user_id: int) -> Income | Expense:
        transaction = self.income_repo.get_by_id_and_user(transaction_id, user_id)

        if not transaction:
            transaction = self.expense_repo.get_by_id_and_user(transaction_id, user_id)

        if not transaction:
            raise ValueError("Transaction not found")

        # check what instance of object is the transaction to use proper repo method
        if isinstance(transaction, Income):
            self.income_repo.delete(transaction)
        else:
            self.expense_repo.delete(transaction)

        return transaction

    # PRIVATE helper methods
    def _convert_transaction(self, old_transaction, new_category, user_id, **kwargs):
        """convert transaction to opposite type"""
        # NOTE: ignore the unhighlighted words as my linter is dumb
        # extract data (new category already validated)
        amount = kwargs.get("amount", old_transaction.amount)
        account_id = kwargs.get("account_id", old_transaction.account_id)
        description = kwargs.get("description", old_transaction.description)
        date_time = kwargs.get("date_time", old_transaction.date_time)

        # delete old
        if isinstance(old_transaction, Income):
            self.income_repo.delete(old_transaction)
            new_type = "expense"
        else:
            self.expense_repo.delete(old_transaction)
            new_type = "income"

        # create new
        if new_type == "income":
            new_transaction = Income(
                amount=amount,
                category_id=new_category.id,
                account_id=account_id,
                description=description,
                date_time=date_time,
                user_id=user_id,
            )
            self.income_repo.save(new_transaction)
        else:
            new_transaction = Expense(
                amount=amount,
                category_id=new_category.id,
                account_id=account_id,
                description=description,
                date_time=date_time,
                user_id=user_id,
            )
            self.expense_repo.save(new_transaction)

        return new_transaction
