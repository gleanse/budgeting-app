from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
import bcrypt

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password_hash: str
    # one to many relationship since one user can have so many incomes thats why its foreignkey to Income table
    incomes: list["Income"] = Relationship(back_populates="user")
    expenses: list["Expense"] = Relationship(back_populates="user")
    categories: list["Category"] = Relationship(back_populates="user")

    # hash password and store it
    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            salt
        ).decode("utf-8")

    # verify if password matches the hash
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), 
            self.password_hash.encode("utf-8")
        )
    
class Income(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # gt means greater than to make sure it wont stored negatives invalid numbers
    amount: float = Field(gt=0)
    category_id: int = Field(foreign_key="category.id")
    description: str
    # default_factory for dynamic values, used lambda to encapsulate the datetime stamp function that only run everytime its recorded or data is being inserted
    date_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: int = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="incomes")
    category: "Category" = Relationship(back_populates="incomes")

class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: float = Field(gt=0)
    category: str = Field(index=True)
    description: str
    date_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: int = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="expenses")
    category: "Category" = Relationship(back_populates="expenses")

class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    type: str = Field()
    user_id: int = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="categories")
    incomes: list["Income"] = Relationship(back_populates="category")
    expenses: list["Expense"] = Relationship(back_populates="category")