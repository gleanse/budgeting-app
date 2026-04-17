from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from datetime import datetime, timezone
import bcrypt


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password_hash: str

    incomes: list["Income"] = Relationship(back_populates="user")
    expenses: list["Expense"] = Relationship(back_populates="user")
    categories: list["Category"] = Relationship(back_populates="user")
    accounts: list["Account"] = Relationship(back_populates="user")

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
    user_id: int = Field(foreign_key="users.id")

    user: User = Relationship(back_populates="categories")
    incomes: list["Income"] = Relationship(back_populates="category")
    expenses: list["Expense"] = Relationship(back_populates="category")


class Account(SQLModel, table=True):
    __tablename__ = "accounts"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    user_id: int = Field(foreign_key="users.id")

    user: User = Relationship(back_populates="accounts")
    incomes: list["Income"] = Relationship(back_populates="account")
    expenses: list["Expense"] = Relationship(back_populates="account")


class Income(SQLModel, table=True):
    __tablename__ = "incomes"

    id: int | None = Field(default=None, primary_key=True)
    # gt(greater than) to avoid negative value
    amount: float = Field(gt=0)
    category_id: int | None = Field(default=None, foreign_key="categories.id")
    description: str
    date_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: int = Field(foreign_key="users.id")
    account_id: int = Field(foreign_key="accounts.id")

    user: User = Relationship(back_populates="incomes")
    category: Category | None = Relationship(back_populates="incomes")
    account: Account = Relationship(back_populates="incomes")


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"

    id: int | None = Field(default=None, primary_key=True)
    amount: float = Field(gt=0)
    category_id: int | None = Field(default=None, foreign_key="categories.id")
    description: str
    date_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: int = Field(foreign_key="users.id")
    account_id: int = Field(foreign_key="accounts.id")

    user: User = Relationship(back_populates="expenses")
    category: Category | None = Relationship(back_populates="expenses")
    account: Account = Relationship(back_populates="expenses")
