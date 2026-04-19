from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from datetime import datetime, timezone
from decimal import Decimal
import bcrypt


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str

    incomes: list["Income"] = Relationship(back_populates="user")
    expenses: list["Expense"] = Relationship(back_populates="user")
    categories: list["Category"] = Relationship(back_populates="user")
    accounts: list["Account"] = Relationship(back_populates="user")
    transfers: list["Transfer"] = Relationship(back_populates="user")
    budgets: list["Budget"] = Relationship(back_populates="user")

    # hash password and store it
    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode(
            "utf-8"
        )

    # verify if password matches the hash
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )


class Category(SQLModel, table=True):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    type: str = Field()
    user_id: int = Field(foreign_key="users.id", index=True)

    user: User = Relationship(back_populates="categories")
    incomes: list["Income"] = Relationship(back_populates="category")
    expenses: list["Expense"] = Relationship(back_populates="category")
    budgets: list["Budget"] = Relationship(back_populates="category")


class Account(SQLModel, table=True):
    __tablename__ = "accounts"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    initial_balance: Decimal = Field(default=Decimal("0.00"))
    user_id: int = Field(foreign_key="users.id", index=True)

    user: User = Relationship(back_populates="accounts")
    incomes: list["Income"] = Relationship(back_populates="account")
    expenses: list["Expense"] = Relationship(back_populates="account")
    transfers_out: list["Transfer"] = Relationship(
        back_populates="from_account",
        sa_relationship_kwargs={"foreign_keys": "[Transfer.from_account_id]"},
    )
    transfers_in: list["Transfer"] = Relationship(
        back_populates="to_account",
        sa_relationship_kwargs={"foreign_keys": "[Transfer.to_account_id]"},
    )


class Budget(SQLModel, table=True):
    __tablename__ = "budgets"
    __table_args__ = (UniqueConstraint("user_id", "category_id", "period_start"),)

    id: int | None = Field(default=None, primary_key=True)
    limit_amount: Decimal = Field(gt=0)
    period_start: datetime
    period_end: datetime
    user_id: int = Field(foreign_key="users.id", index=True)
    category_id: int = Field(foreign_key="categories.id", index=True)

    user: User = Relationship(back_populates="budgets")
    category: Category = Relationship(back_populates="budgets")


class Transfer(SQLModel, table=True):
    __tablename__ = "transfers"

    id: int | None = Field(default=None, primary_key=True)
    amount: Decimal = Field(gt=0)
    from_account_id: int = Field(foreign_key="accounts.id", index=True)
    to_account_id: int = Field(foreign_key="accounts.id", index=True)
    description: str | None = Field(default=None)
    date_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )
    user_id: int = Field(foreign_key="users.id", index=True)

    user: User = Relationship(back_populates="transfers")
    from_account: Account = Relationship(
        back_populates="transfers_out",
        sa_relationship_kwargs={"foreign_keys": "[Transfer.from_account_id]"},
    )
    to_account: Account = Relationship(
        back_populates="transfers_in",
        sa_relationship_kwargs={"foreign_keys": "[Transfer.to_account_id]"},
    )


class Income(SQLModel, table=True):
    __tablename__ = "incomes"

    id: int | None = Field(default=None, primary_key=True)
    amount: Decimal = Field(gt=0)
    category_id: int | None = Field(
        default=None, foreign_key="categories.id", index=True
    )
    description: str
    date_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )
    user_id: int = Field(foreign_key="users.id", index=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)

    user: User = Relationship(back_populates="incomes")
    category: Category | None = Relationship(back_populates="incomes")
    account: Account = Relationship(back_populates="incomes")


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"

    id: int | None = Field(default=None, primary_key=True)
    amount: Decimal = Field(gt=0)
    category_id: int | None = Field(
        default=None, foreign_key="categories.id", index=True
    )
    description: str
    date_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )
    user_id: int = Field(foreign_key="users.id", index=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)

    user: User = Relationship(back_populates="expenses")
    category: Category | None = Relationship(back_populates="expenses")
    account: Account = Relationship(back_populates="expenses")
